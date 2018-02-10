Title: x264 Slice Type Decision
Date: 2017-12-06
Category: Technology  
Tags: Video Codec, x264 
Slug: x264_slice_type_decision

#### __Outline__
***

Doc of [MB Tree]({attach}/blogs/blog_12_06_2017_x264_slice_type_decision/MBtree paper.pdf)

    
#### __Process__
***
The x264 decide slice type in a GOP structure unit, which include one reference frame (I,P) and no / several non-reference frame (B). The processed frame will be shift out frame lookahead frame list and put into frame's current list.

    if( !h->frames.current[0] )
        x264_lookahead_get_frames( h );
        
The slice type analyse and decide was first handle in `x264_lookahead_get_frames`. The function will call `x264_slicetype_decide` and `x264_slicetype_analyse`. 

    x264_stack_align( x264_slicetype_decide, h );
    /* For MB-tree and VBV lookahead, we have to perform propagation analysis on I-frames too. */
    if( h->lookahead->b_analyse_keyframe && IS_X264_TYPE_I( h->lookahead->last_nonb->i_type ) )
        x264_stack_align( x264_slicetype_analyse, h, shift_frames );

<span style="color:green;">*x264_slicetype_decide*</span>
***
1. The lookahead routine accumulate many frame in it's queue for analyse. The frames in list `next` in lookahead structure are waiting for process. The first part of `x264_slicetype_decide` is to calculate the duration of each frame in the lookahead list `next`

2. If user choose 2-pass rate control the slice type has been analysed and decide in the 1st-pass. Thus, at current stage, just need to read the result of the 1st-pass. Otherwise, call `x264_slicetype_analyse`, which will be analyse in the following section.

        if( h->param.rc.b_stat_read )
            x264_ratecontrol_slice_type();
        else if(...)
            x264_slicetype_analyse();

    As stated above, slice type analyse will determine slice type in a gop.  
    
3. Calculate the frame costs ahead of time for x264_rc_analyse_slice while still have lowres. The frame cost will be used for rate control. 


<span style="color:green;">*x264_slicetype_analyse*</span>
*** 

The `x264_slicetype_analyse` focus on the following tasks:

1.  
    Decide the frame type. For non-b setting, actully, the slice type decision is straightforward that keyframe (IDR/I) followed by interframe (P).
    
    For sequence with B frame, x264 propose two B adaptive algorithm `X264_B_ADAPT_FAST` and `X264_B_ADAPT_TRELLIS` and one non-adaptive algorithm `X264_B_ADAPT_NONE`.
    
    For `X264_B_ADAPT_NONE`, the encoder will follow the gop structure constructed by keyframe intervel, bframe number, etc. For example, if user set `--bframes 2` and `--keyint 30`. The encoded gop structure will be IPBBPBBPBB... with IDR picture appear every 30 frames.
    
    The `X264_B_ADAPT_TRELLIS` is complicate and slow, we will <span style="color:blue;">discuss in the future</span>.
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    