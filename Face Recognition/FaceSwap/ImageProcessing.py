import numpy as np
import cv2

# here src is the image from which the pixels will be pasted into the dst image
# feather amount is a percentage that controls the size of the area to be weighted


def blendImages(src, dst, mask, featherAmount=0.2):

    # non-black pixel indices of the mask
    maskIndices = np.where(mask != 0)
    # the same indices, but now in one matrix, where each row is one pixel (x, y)
    maskPts = np.hstack(
        (maskIndices[1][:, np.newaxis], maskIndices[0][:, np.newaxis]))
    faceSize = np.max(maskPts, axis=0) - np.min(maskPts, axis=0)
    featherAmount = featherAmount * np.max(faceSize)

    hull = cv2.convexHull(maskPts)
    dists = np.zeros(maskPts.shape[0])
    for i in range(maskPts.shape[0]):
        dists[i] = cv2.pointPolygonTest(
            hull, (maskPts[i, 0], maskPts[i, 1]), True)

    weights = np.clip(dists / featherAmount, 0, 1)

    composedImg = np.copy(dst)
    composedImg[maskIndices[0], maskIndices[1]] = weights[:, np.newaxis] * src[maskIndices[0],
                                                                               maskIndices[1]] + (1 - weights[:, np.newaxis]) * dst[maskIndices[0], maskIndices[1]]

    return composedImg

# attention, here src is the image from which the color will be taken


def colorTransfer(src, dst, mask):
    transferredDst = np.copy(dst)
    # non-black pixel indices of the mask
    maskIndices = np.where(mask != 0)
    # src [maskIndices [0], maskIndices [1]] returns the pixels in the non-black area of ​​the mask

    maskedSrc = src[maskIndices[0], maskIndices[1]].astype(np.int32)
    maskedDst = dst[maskIndices[0], maskIndices[1]].astype(np.int32)

    meanSrc = np.mean(maskedSrc, axis=0)
    meanDst = np.mean(maskedDst, axis=0)

    maskedDst = maskedDst - meanDst
    maskedDst = maskedDst + meanSrc
    maskedDst = np.clip(maskedDst, 0, 255)

    transferredDst[maskIndices[0], maskIndices[1]] = maskedDst

    return transferredDst
