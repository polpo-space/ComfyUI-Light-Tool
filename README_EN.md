# ComfyUI-Light-Tool

**English** / [简体中文](./README.md)

A suite of lightweight and practical custom tool nodes for ComfyUI to enhance workflow efficiency and flexibility.

---

## 📦 Installation Guide

### 1. Manual Installation

```bash
# Navigate to the custom_nodes directory of ComfyUI
cd ComfyUI/custom_nodes

# Clone this repository
git clone https://github.com/ihmily/ComfyUI-Light-Tool.git

# Restart ComfyUI
```

### 2. Installation via ComfyUI-Manager

Automatic installation through ComfyUI-Manager:

1. Go to the **Manager** panel in the ComfyUI interface.
2. Under the **Custom Nodes** tab, search for `ComfyUI-Light-Tool`.
3. Click **Install** and restart ComfyUI.

---

## 🎨 Functional Categories and Node List

### 1. Image Processing

| Node Name                                                    | Function Description                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Load Image**                                               | Load local image files (supports preserving RGBA transparency). |
| **Load Image From URL**                                      | Download and load images from a URL.                         |
| **Load Image List**                                          | Batch load images from a directory.                          |
| **Image Overlay**                                            | Combine two images (requires consistent size and mask).      |
| **Simple Image Overlay**                                     | Overlay images freely (with adjustable positioning).         |
| **Image Concat**                                             | Concatenate multiple images horizontally or vertically.      |
| **Resize Image** / **Resize Image V2** / **Resize by Ratio/Max Size** | Flexibly adjust image size, ratio, or maximum dimensions.    |
| **Scale Image**                                              | Scale images using algorithms.                               |
| **Upscale Image**                                            | Upscale images using algorithms.                             |
| **Add Solid Color Background**                               | Add a solid color background to transparent images.          |
| **Image to Mask** / **Mask to Image**                        | Convert between images and masks.                            |
| **Invert Mask**                                              | Invert mask colors.                                          |
| **Bounding Box Cropping**                                    | Crop images based on coordinates.                            |
| **RGB to RGBA** / **RGBA to RGB**                            | Convert between image color channels.                        |
| **Morphological Transform**                                  | Perform morphological operations on masks (e.g., erosion, dilation). |
| **Extract Transparent Image**                                | Extract foreground transparent images from the original using a mask. |
| **Mask Background to Transparent**                           | Convert non-mask areas in mask images to transparency.       |

### 2. Text Processing

| Node Name                                                  | Function Description               |
| ---------------------------------------------------------- | ---------------------------------- |
| **Input Text**                                             | Input text.                        |
| **Input Text List**                                        | Input a list of texts.             |
| **Connect Text Strings** / **Simple Connect Text Strings** | Concatenate multiple text strings. |
| **Show Text**                                              | Display text content.              |

### 3. Video Related

| Node Name         | Function Description                     |
| ----------------- | ---------------------------------------- |
| **Load Video**    | Load videos (from video URLs).           |
| **Preview Video** | Preview video content (from video URLs). |
| **Save Video**    | Save videos to a local directory.        |

### 4. Data Processing

| Node Name                      | Function Description                                         |
| ------------------------------ | ------------------------------------------------------------ |
| **Get Image Size**             | Obtain image width, height, and file size information.       |
| **Hex to RGB**                 | Convert hexadecimal color codes to RGB values.               |
| **Calculate**                  | Perform numerical calculations (e.g., addition, subtraction, multiplication, division, percentages). |
| **Convert Num Type**           | Convert numerical types (integer/float/string).              |
| **Get Images Count**           | Count the number of images in a list.                        |
| **KeyValue**                   | Extract key-value pairs from JSON data.                      |
| **Serialize/Deserialize JSON** | Serialize or deserialize JSON objects.                       |

### 5. Practical Tools

| Node Name                                      | Function Description                                         |
| ---------------------------------------------- | ------------------------------------------------------------ |
| **PhantomTankEffect**                          | Generate "Phantom Tank" effects.                             |
| **Is Transparent**                             | Detect whether an image is transparent.                      |
| **Mask Bounding Box Cropping**                 | Crop images based on mask boundaries.                        |
| **Save to Signed PUT URL**                     | Upload files through a presigned PUT URL.                    |
| **Save Metadata** / **Load Metadata From URL** | Save or load metadata (e.g., image descriptions, parameters). |
| **SolidColorBackground**                       | Generate custom solid color background images.               |

---

## Wownow Process Config

`Light-Tool: DeserializeWownowProcessConfig` accepts a JSON string for image dimensions, the origin image URL, and server-issued presigned PUT upload URLs. Go callers can generate that JSON with this struct:

```go
type WownowProcessConfig struct {
	Width          int    `json:"width"`
	Height         int    `json:"height"`
	OriginImageURL string `json:"origin_image_url"`

	UVImagePutURL        string `json:"uv_image_put_url"`
	BinaryImagePutURL    string `json:"binary_image_put_url"`
	DepthImagePutURL     string `json:"depth_image_put_url"`
	NormalmapImagePutURL string `json:"normalmap_image_put_url"`
	OutpaintImagePutURL  string `json:"outpaint_image_put_url"`
}
```

The `*_put_url` fields currently carry presigned PUT URLs and can be connected directly to the `put_url` input of `Light-Tool: SaveToSignedPutURL`.

---

## 🛠️ Development and Contribution

- **Feedback**: Submit issues via [GitHub Issues](https://github.com/ihmily/ComfyUI-Light-Tool/issues).
- **Code Contribution**: Fork the repository and submit a Pull Request.
- **Documentation Updates**: Report any inaccuracies or omissions in the descriptions.

---

## 📖 License

This project is licensed under the [MIT License](LICENSE).
