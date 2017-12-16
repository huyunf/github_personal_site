Title: x264 Rate Control
Date: 2017-12-05
Category: Technology  
Tags: Video Codec, x264 
Slug: x264_rate_control

#### __Outline__
***

Rate control allows selection of encoding parameters to maximize quality under the constraint imposed by specified bitrate and decoder video buffer. The rate control in H.264/AVC can be performed at three different granularities – group of pictures level, picture level and macroblocks level. At each level, the rate control selects quantization parameter (QP) values, that determine the quantization of transform coefficients. Increase in QP increases quantization step size and decreases the bitrate. The rate control in x264 is based upon libavcodec's implementation, and is mostly empirical. There are five different rate control modes in x264 and are described below. In the hypothetical reference decoder (VBV) mode, x264 allows each macroblock to have a different QP, while in other modes QP is determined for an entire frame.

*Two pass (2pass)*

In this approach, data is obtained about each frame during a first pass, allowing x264 to allocate bits globally over the file.

*Average bitrate (ABR)*

This is a one-pass scheme where the rate control must be done without knowledge of future frames.

1. run a fast motion estimation algorithm over a half-resolution version of the frame, and use the Sum of Absolute Hadamard Transformed Differences (SATD) of the residuals as the complexity. Also, the complexity of the following GOP is unknown, so I-frame QPs are based on the past. 

2. We do not know the complexities of future frames, so we can only scale based on the past. The scaling factor is chosen to be the one that would have resulted in the desired bitrate if it had been applied to all frames so far.

3. Long and short term compensation is the same as in 2pass. By tuning the strength of compensation, it is possible to obtain quality ranging from close to 2pass (but with file size error of ±10%) to lower quality with reasonably strict file size.

*VBV-compliant constant bitrate (CBR)*

This is a one-pass mode designed for real-time streaming.

1. It uses the same complexity estimation for computing bit size as ABR.

2. The scaling factor used for achieving the requested file-size is based on a local average (dependent on VBV buffer size) instead of all past frames.

3. The overflow compensation is the same algorithm as in ABR, but runs after each row of macroblocks instead of per-frame.

*Constant rate-factor*

This is a one-pass mode that is optimal if the user does not desire a specific bitrate, but specifies quality instead. It is the same as ABR, except that the scaling factor is a user defined constant and no overflow compensation is done.

*Constant quantizer*

This is a one-pass mode where QPs are simply based on whether the frame is I-, P- or Bframe.

#### __Process__
***

For this section, we don't discuss the two pass algorithm, only focus on one pass rate control algorithm.

*x264_ratecontrol_new @ x264_encoder_open*
    
* initial parameters like fps, bitrate...

* `x264_ratecontrol_init_reconfigurable`: special parameters initial for CRF & VBV_CBR rate control

* set mb level qp adjustable flag: b_variable_qp if VBV_CBR or aq_mode enabled: 

        h->mb.b_variable_qp = rc->b_vbv || h->param.rc.i_aq_mode;

* if use ABR, initial complex sum as 
    
        rc->cplxr_sum = .01 * pow( 7.0e5, rc->qcompress ) * pow( h->mb.i_mb_count, 0.5 );
    
* set qp offset for P and B frame:

        rc->ip_offset = 6.0 * log2f( h->param.rc.f_ip_factor );
        rc->pb_offset = 6.0 * log2f( h->param.rc.f_pb_factor );

* get level step according to qp step:
        
        rc->lstep = pow( 2, h->param.rc.i_qp_step / 6.0 );
        
















    
    
    
    
    
    
    
    