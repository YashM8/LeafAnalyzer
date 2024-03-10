from plantcv import plantcv as pcv
import os


def process_image(image_path, output_path, plot=False):
    try:
        img, filename, path = pcv.readimage(filename=image_path)
    except RuntimeError:
        print(f"\n\nCould not find file at - {image_path}\n\n")
        return

    # Define the region of interest (ROI) as the entire image
    roi = pcv.roi.rectangle(img=img, x=0, y=0, h=img.shape[0], w=img.shape[1])

    # Apply Gaussian blur to the image
    gaussian_img = pcv.gaussian_blur(img=img, ksize=(35, 35), sigma_x=0, sigma_y=None)

    # Convert to grayscale
    a_gray = pcv.rgb2gray_lab(rgb_img=gaussian_img, channel="b")

    # Apply triangle thresholding (B&W)
    thresh = pcv.threshold.triangle(gray_img=a_gray, object_type="light")

    # Fill in the missed points in thresholding
    fill_image = pcv.fill(bin_img=thresh, size=300)

    # Filter the filled objects to keep only those within the ROI
    kept_mask = pcv.roi.filter(mask=fill_image, roi=roi, roi_type='partial')

    # Create labels for the connected objects
    labeled_objects, n_obj = pcv.create_labels(mask=kept_mask)

    # Extract dimensions and data
    analysis_image = pcv.analyze.size(img=img, labeled_mask=labeled_objects, n_labels=n_obj)

    if plot:
        pcv.plot_image(analysis_image)

    try:
        pcv.outputs.save_results(filename=output_path)
    except FileNotFoundError:
        print(f"\n\nCould not save.\n\n")

    print(f"\nProcessed file - {os.path.basename(image_path)}\n {n_obj} objects\n")


process_image(image_path="../test_images/test2.png",
              output_path="../measured_data/test2.json",
              plot=True)
