Title: H264 De-blocking Filter
Date: 2017-11-20
Category: Technology  
Tags: Video Codec, h264 
Slug: h264_deblocking_algorithm

#### __Introduction__
***

A deblocking filter is a video filter applied to decoded compressed video to improve visual quality and prediction performance by smoothing the sharp edges which can form between macroblocks when block coding techniques are used. Here is an [artical]({attach}/blog/blog_11_21_2017_h264_algorithm/cr1261.pdf) and [web page](https://www.vcodex.com/h264avc-loop-filter/) introduce the H264 in-loop filter.

#### __Description of In-loop De-blocking Filter__
***

A filter is applied to every decoded macroblock in order to reduce blocking distortion. The deblocking filter is applied after the inverse transform in the encoder (before reconstructing and storing the macroblock for future predictions) and in the decoder (before reconstructing and displaying the macroblock).

The filter has two benefits: 

* block edges are smoothed, improving the appearance of decoded images (particularly at higher compression ratios)
* the filtered macroblock is used for motion-compensated prediction of further frames in the encoder, resulting in a smaller residual after prediction. (Note: intra-coded macroblocks are filtered, but intra prediction is carried out using unfiltered reconstructed macroblocks to form the prediction). Picture edges are not filtered.

Filtering is applied to vertical or horizontal edges of 4x4 blocks in a macroblock, in the following order:

1. Filter 4 vertical boundaries of the luma component (in order a,b,c,d)
2. Filter 4 horizontal boundaries of the luma component (in order e,f,g,h)
3. Filter 2 vertical boundaries of each chroma component (i,j)
4. Filter 2 horizontal boundaries of each chroma component (k,l)

![Photo]({attach}/blog/blog_11_21_2017_h264_algorithm/h264_deblocking_edge.png){width=80%}

Each filtering operation affects up to three pixels on either side of the boundary. Figure 2 shows 4 pixels on either side of a vertical or horizontal boundary in adjacent blocks p and q (p0,p1,p2,p3 and q0,q1,q2,q3). Depending on the current quantizer, the coding modes of neighbouring blocks and the gradient of image samples across the boundary, several outcomes are possible, ranging from (a) no pixels are filtered to (b) p0, p1, p2, q0, q1, q2 are filtered to produce output pixels P0, P1, P2, Q0, Q1 and Q2.

![Photo]({attach}/blog/blog_11_21_2017_h264_algorithm/h264_deblocking_pixel.png){width=80%}

#### __Boundary strength__
***

The choice of filtering outcome depends on the boundary strength and on the gradient of image samples across the boundary. The boundary strength parameter Bs is chosen according to the following rules:

![Photo]({attach}/blog/blog_11_21_2017_h264_algorithm/h264_deblocking_BS.png){width=80%}

#### __Filter decision__
***

A group of samples from the set (p2,p1,p0,q0,q1,q2) is filtered only if:

* Bs > 0 and
* |p0-q0|, |p1-p0| and |q1-q0| are each less than a threshold $\alpha$ or $\beta$ ($\alpha$ and $\beta$ are defined in the standard). 

The thresholds $\alpha$ and $\beta$ increase with the average quantizer parameter QP of the two blocks p and q. The purpose of the filter decision is to “switch off” the filter when there is a significant change (gradient) across the block boundary in the original image. The definition of a significant change depends on QP. When QP is small, anything other than a very small gradient across the boundary is likely to be due to image features (rather than blocking effects) that should be preserved and so the thresholds $\alpha$ and $\beta$ are low. When QP is larger, blocking distortion is likely to be more significant and $\alpha$ and $\beta$ are higher so that more filtering takes place.

#### __Filter implementation__
***

(a) Bs = {1,2,3}:

A 4-tap linear filter is applied with inputs p1, p0, q0 and q1, producing filtered outputs P0 and Q0(0<Bs<4).

In addition, if |p2-p0| is less than threshold β, a 4-tap linear filter is applied with inputs p2, p1, p0 and q0, producing filtered output P1. If |q2-q0| is less than threshold β, a 4-tap linear filter is applied with inputs q2, q1, q0 and p0, producing filtered output Q1. (p1 and q1 are never filtered for chroma, only for luma data).

(b) Bs = 4:

	If |p2-p0|<β and |p0-q0|<round(α/4):
		P0 is produced by 5-tap filtering of p2, p1, p0, q0 and q1 
		P1 is produced by 4-tap filtering of p2, p1, p0 and q0 
		(Luma only) P2 is produced by 5-tap filtering of p3, p2, p1, p0 and q0.
	else:
		P0 is produced by 3-tap filtering of p1, p0 and q1.

	If |q2-q0|<β and |p0-q0|<round(α/4):
		Q0 is produced by 5-tap filtering of q2, q1, q0, p0 and p1
		Q1 is produced by 4-tap filtering of q2, q1, q0 and p0
		(Luma only) Q2 is produced by 5-tap filtering of q3, q2, q1, q0 and p0.
	else:
		Q0 is produced by 3-tap filtering of q1, q0 and p1.












