Title: x264 Encoder Open
Date: 2017-11-20
Category: Technology  
Tags: Video Codec, x264 
Slug: x264_encoder_open

#### __Outline__
***
In this chapter, we make a brief review of `x264_encoder_open' function. In this function, x264 mainly did several jobs like 
    
    x264_threading_init                             // initial thread
    x264_validate_parameters                        // validate the configure parameters
    x264_sps_init                                   // initial sps parameters
    x264_pps_init                                   // initial pps parameters
    x264_cqm_init                                   // quant & dequant parameters initial
    Init frames parameters, such as max reference numbers, rc related..
    x264_rdo_init                                   // rate distortion parameters initial
    x264_predict_xxx_init ~ x264_bitstream_xxx_init // register function for function pointers
    x264_cabac_init || x264_cavlc_init              // initial entropy encoding parameters
    x264_analyse_init_costs                         // prepare parameters be used to calc cost in analyse step
    x264_threadpool_init                            // x264 thread pool prepare
    x264_lookahead_init                             // buffer & parameters prepare for lookahead routine
    x264_ratecontrol_new                            // rate control start

#### __Function Brief__
***

*   _x264_threading_init_:

    Did some kernel level check / initial for thread supportting

*   _x264_validate_parameters_:
    
    Check if the input configuration parameters are valid. Such as whether the widht/height violate the max resolution constraint, whether some enabled feature violate with the profile / level

*   _x264_cqm_init_:
    
    Pre-calculate the quan & dequant parameters. For q/dq algorithm, please refer to ...

*   _x264_rdo_init_:
        
    Initialize the bit cost (MV) array accordint to CABAC state trasition
    
*   _x264_predict_xxx_init ~ x264_bitstream_xxx_init_:
    
    Funtion pointer initialization for those utility function like prediection, dct. etc
    
*   _x264_cabac_init_:
    
    The cabac initial algorithm detail, please refer to [Entropy Coding]({filename}/blogs/blog_11_21_2017_h264_algorithm/blog_11_21_2017_h264_entropy.md)

        void x264_cabac_init( x264_t *h )
        {
            int ctx_count = CHROMA444 ? 1024 : 460;
            for( int i = 0; i < 4; i++ )
            {
                const int8_t (*cabac_context_init)[1024][2] = i == 0 ? &x264_cabac_context_init_I
                                                                     : &x264_cabac_context_init_PB[i-1];
                for( int qp = 0; qp <= QP_MAX_SPEC; qp++ )
                    for( int j = 0; j < ctx_count; j++ )
                    {
                        int state = x264_clip3( (((*cabac_context_init)[j][0] * qp) >> 4) + (*cabac_context_init)[j][1], 1, 126 );
                        x264_cabac_contexts[i][qp][j] = (X264_MIN( state, 127-state ) << 1) | (state >> 6);
                    }
            }
        }
    
    For x264, each entry of context is:
    
    $min(\sigma_{pre}, 127-\sigma_{pre})<<1 | (\sigma_{pre}>>6)$
    
    which put the $\varpi$ in LSB, that is:
    
    if ($\sigma_{pre} \leq 63$) $\sigma_{pre} | (\sigma_{pre}>>6)$
        
    else $(127-\sigma_{pre})<<1 | (\sigma_{pre}>>6)$
        
*   _x264_analyse_init_costs_:
    
    Initial a cost table for refernce selection & mv decision. The cost table was build for each possible qp. 
    
    step 1: initial logs array:
    
        logs[0] = 0.718f;
        for( int i = 1; i <= 2*4*2048; i++ )
            logs[i] = log2f( i+1 ) * 2.0f + 1.718f;
    
    step 2: build up cost table:
        
        // MV cost
        lambda = pow(2,qp/6-2)
        for( int i = 0; i <= 2*4*2048; i++ )
            h->cost_mv[qp][-i] = h->cost_mv[qp][i] = X264_MIN( lambda * logs[i] + .5f, (1<<16)-1 );
    
        // ref cost
        for( int i = 0; i < 3; i++ )
        for( int j = 0; j < 33; j++ )
            x264_cost_ref[qp][i][j] = X264_MIN( i ? lambda * bs_size_te( i, j ) : 0, (1<<16)-1 );
    
        // frac MV cost
        for( int i = -2*2048; i < 2*2048; i++ )
            h->cost_mv_fpel[qp][j][i] = h->cost_mv[qp][i*4+j];
    
        // mode cost: 9 for intra 8 for inter? 16x16, 16x8, 8x16, 8x8, 8x8, 8x4, 4x8, 4x4
        for( int i = 0; i < 17; i++ )
            cost_i4x4_mode[i] = 3*lambda*(i!=8);
    
    
*   _x264_lookahead_init_:
    
    Initial several parameters and frame list for lookahead routine.
    
    lookahead is a process before real encoding. It contain the process of abq, rc, slice decision. etc. Once it was malloc, each thread will get it:
    
        for( int i = 0; i < h->param.i_threads; i++ )
            h->thread[i]->lookahead = look;
    
    lookahead process contain 3 frame list: ifbuf, next, ofbuf. When frame's loweres prepared, the frame will be put into ifbuf(input buffer list) if multithread support. If there is only one thread, it will be put into next. After lookahead process end, the frame will be put into ofbuf (output buffer list). Then the real encoding process could get frame will lookahead ready from ofbuf list.
    
*   _x264_ratecontrol_new_:
    
    Please refer to [x264 rate control]({filename}/blogs/blog_12_05_2017_x264_rate_control/blog_12_05_2017_x264_rate_control.md) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    