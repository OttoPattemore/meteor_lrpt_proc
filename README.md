# Meteor LRPT Proc
Process images from Meteor M2 LRPT.
## Setup
```bash
# Install dependencies
pip3 install Pillow

# Run the processor
python3 meteor_lrpt_proc.py <RGB221_image> <Thermal_image> <Output_Directory>
```

## Supported processors
|Name|Status|
|----|------|
|Veg        🌳| Stable|
|Rainfall   🌧| Stable|
|No Veg     🏜| Stable|

## Examples

### Vegetation 🌳
![Vegetation Processor Result](/example_results/veg.png)

### No Vegetation 🏜
![No Vegetation Processor Result](/example_results/noveg.png)

### Rainfall 🌧
![Rainfall Map](/example_results/rainfall.png)
