Title: x264 Encoder Open
Date: 2017-11-20
Category: Technology  
Tags: Video Codec, h264, x264 
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
        
    Initialize the bit cost array accordint to CABAC state trasition
    
*   _x264_predict_xxx_init ~ x264_bitstream_xxx_init_:
    
    Funtion pointer initialization for those utility function like prediection, dct. etc
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    