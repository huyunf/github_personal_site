Title: x264 Adaptive Quant
Date: 2017-12-06
Category: Technology  
Tags: Video Codec, x264 
Slug: x264_adaptive_quant

#### __Outline__
***
    
Adaptive Quant is claimed as the biggest performance improvement of x264 optimization history. According to AQ's author Jason Garrett-Glaser's explaination [variance-based adaptive quantization](https://mailman.videolan.org/pipermail/x264-devel/2012-July/009403.html)
    
    The (very rough) intuitive justification works something like this. Imagine every macroblock has just one frequency coefficient.  This coefficient can be big or small.

    If a macroblock's coefficient is 1.4, it gets quantized to 1.  That's an error of 28.5%.

    If a macroblock's coefficient is 9.4, it gets quantized to 9.  That's an error of 4.3%.

    Clearly, larger coefficients are coded more precisely than smaller ones when using a linear quantizer.  Visually, it is obvious this is somewhat wrong; just because a detail is 10 times higher-contrast in block X than block Y doesn't mean block Y should be completely decimated.

    One solution to this would be to use a nonlinear quantizer like in AAC.  Obviously this is not possible without changing the H.264 spec, and would also be much slower.  Turns out that it's actually not that useful from my own testing -- this is because large coefficients in a block tend to mask small coefficients.  If you have a few big ones, there's no point in coding the small ones with tons of precision.

    Since quantizer in H.264 is exponential, using log2(variance) to change QP is equivalent to using (variance) to change quantizer step size.  Therefore:

    qp += log(variance)*C
    qp = qp + log(variance) * C
    e^qp = e^(qp + log(variance) * C)
    qscale = qscale * e^(log(variance)*C)
    qscale = qscale * variance^C
    qscale *= variance^C

    The constant C was decided through wild guessing and experimentation and is based on nothing in particular.

    As it happens, SSIM basically is PSNR weighted by variance in a similar fashion, albeit less explicitly so.

The x264 AQ algorithm have 3 mode: `X264_AQ_VARIANCE`, `X264_AQ_AUTOVARIANCE` and `X264_AQ_AUTOVARIANCE_BIASED`, plus the none AQ mode `X264_AQ_NONE`
    
#### __Process__
***
    
*initial qp offset -> x264_adaptive_quant_frame @ x264_encoder_encode*

*   _energy_:

Before introduce how x264 get qp adjust value for each MB, we need to introduce how it define energy. In AQ mode calc, it define energy as [variance](https://en.wikipedia.org/wiki/Variance)

    E[X^2] - E[X]^2 = ssd - (sum * sum >> shift)

*   _brief_:

The main purpose of this function is to initialize the parameter `qp_offset` for each MB. 

There are two input parameters control the result of aq mode:

rc.i_aq_mode: (0~3). (1) X264_AQ_NONE[0]->no aq mode (2)X264_AQ_VARIANCE[1]->mb tree mode (3)       X264_AQ_AUTOVARIANCE [3]  (4) X264_AQ_AUTOVARIANCE_BIASED(3)

rc.f_aq_strength: The value should be less than 1 and smaller the better when film has much details and complex structure such as "animation" (0.6) and film with "grain" characteristic (0.5). The value should be larger than 1 and bigger the better when film has much plain area such as "still image" (1.2) or "touhou" (1.3).

*   _step 1: get qp_adj, strength, etc._:

For mode 'X264_AQ_NONE' or f_aq_strength==0, which mean the MB level adaptive quantization is disabled. So the f_qp_offset are set to '0' or external input value. 

For mode `X264_AQ_AUTOVARIANCE` and `X264_AQ_AUTOVARIANCE_BIASED`, first step is to initial `avg_adj`, `strength` and `bias_strength`

    for( int mb_y = 0; mb_y < h->mb.i_mb_height; mb_y++ )
        for( int mb_x = 0; mb_x < h->mb.i_mb_width; mb_x++ )
        {
            uint32_t energy = x264_ac_energy_mb( h, mb_x, mb_y, frame );
            float qp_adj = powf( energy * bit_depth_correction + 1, 0.125f );
            frame->f_qp_offset[mb_x + mb_y*h->mb.i_mb_stride] = qp_adj;
            avg_adj += qp_adj;
            avg_adj_pow2 += qp_adj * qp_adj;
        }

The larger the "energy" (variance), the bigger the qp adjust value.

For these two mode, their strength and average adjustment is obtained by:

    avg_adj /= h->mb.i_mb_count;
    avg_adj_pow2 /= h->mb.i_mb_count;
    strength = h->param.rc.f_aq_strength * avg_adj;
    avg_adj = avg_adj - 0.5f * (avg_adj_pow2 - 14.f) / avg_adj;
    bias_strength = h->param.rc.f_aq_strength;

For mode `X264_AQ_VARIANCE`, the `aq_adj` will be calc later, only need to adjust strength
    
    strength = h->param.rc.f_aq_strength * 1.0397f;

*   _step 2: calcualte qp adjust for each mb_:

The second step is to calc the qp adjustment:

    if( h->param.rc.i_aq_mode == X264_AQ_AUTOVARIANCE_BIASED )
    {
        qp_adj = frame->f_qp_offset[mb_xy];
        qp_adj = strength * (qp_adj - avg_adj) + bias_strength * (1.f - 14.f / (qp_adj * qp_adj));
    }
    else if( h->param.rc.i_aq_mode == X264_AQ_AUTOVARIANCE )
    {
        qp_adj = frame->f_qp_offset[mb_xy];
        qp_adj = strength * (qp_adj - avg_adj);
    }
    else
    {
        uint32_t energy = x264_ac_energy_mb( h, mb_x, mb_y, frame );
        qp_adj = strength * (x264_log2( X264_MAX(energy, 1) ) - (14.427f + 2*(BIT_DEPTH-8)));
    }
    ...
    frame->f_qp_offset[mb_xy] = frame->f_qp_offset_aq[mb_xy] = qp_adj;
    
Then the qp offset table for each MB has been generated.


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    