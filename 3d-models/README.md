# 3D Printed Club Environment

Complete 3D printable models for the miniature DJ club setup, designed by Kire Angelov based on the original architectural work by the Gradezna Struka program.

## Overview

This directory contains all CAD models and STL files needed to recreate the physical club environment. The models are optimized for FDM 3D printing and designed to integrate with the electronic components (displays, LEDs, motors).

## Models Included

### DJ Booth (`dj-booth/`)

The main performance area featuring integrated display mounts and cable management.

**Files:**
- `booth-main.stl` - Main booth structure with display cutouts
- `booth-screen-mount.stl` - Mounting brackets for ILI9341 displays (3x)
- `booth-base.stl` - Stable base platform
- `assembly-instructions.pdf` - Step-by-step assembly guide

**Features:**
- Precision cutouts for 3x 240x320 displays
- Integrated cable routing channels
- LED mounting points for stage lighting
- Modular design for easy assembly

**Print Settings:**
- Material: PLA or PETG
- Layer Height: 0.2mm
- Infill: 20%
- Supports: Yes (for overhangs)
- Estimated Time: 12-18 hours
- Filament: ~300g

### Bar Counter (`bar/`)

Club bar setup with LED backlighting integration.

**Files:**
- `bar-counter.stl` - Main counter structure
- `bar-shelves.stl` - Interior shelving for bottles/decoration
- `bar-back-panel.stl` - Rear panel with LED mounts
- `assembly-instructions.pdf` - Assembly guide

**Features:**
- Realistic bar counter design
- Integrated shelving system
- LED strip mounting channels
- Decorative panel details

**Print Settings:**
- Material: PLA
- Layer Height: 0.2mm
- Infill: 15%
- Supports: Yes
- Estimated Time: 8-12 hours
- Filament: ~250g

### Tables (`tables/`)

Modular audience seating with multiple size options.

**Files:**
- `table-top-large.stl` - Large round table top
- `table-top-small.stl` - Small round table top
- `table-legs.stl` - Universal table legs with stability base
- `assembly-instructions.pdf` - Assembly guide

**Features:**
- Two table sizes for layout flexibility
- Stable base design
- Realistic proportions
- Easy assembly (press-fit or glue)

**Print Settings:**
- Material: PLA
- Layer Height: 0.2mm
- Infill: 15%
- Supports: No
- Estimated Time: 3-5 hours per table
- Filament: ~80g per table

### Sliding Walls (`sliding-walls/`)

Motorized wall system with integrated stepper motor mounts and limit switches.

**Files:**
- `wall-panel.stl` - Wall panel (print 3x)
- `wall-track.stl` - Linear guide track system
- `motor-mount.stl` - 28BYJ-48 stepper motor mounting bracket (3x)
- `limit-switch-bracket.stl` - Limit switch mounting (2x)
- `assembly-instructions.pdf` - Complete mechanical assembly guide

**Features:**
- Gear system designed by Filip Mihailov
- Compatible with 28BYJ-48 stepper motors
- Integrated limit switch mounts
- Smooth sliding mechanism

**Print Settings:**
- Material: PLA (walls), PETG (motor mounts)
- Layer Height: 0.2mm
- Infill: 10% (walls), 50% (motor mounts)
- Supports: Yes (motor mounts only)
- Estimated Time: 6-8 hours per wall, 3-4 hours per motor mount
- Filament: ~400g total

## Complete Project Printing Summary

| Component | Quantity | Print Time | Filament | Priority |
|-----------|----------|------------|----------|----------|
| DJ Booth | 1 set | 12-18h | 300g | High |
| Bar Counter | 1 set | 8-12h | 250g | Medium |
| Tables | 3-5 sets | 3-5h each | 80g each | Low |
| Sliding Walls | 1 set | 18-24h | 400g | High |
| **Total** | - | **40-60h** | **~1200g** | - |

**Estimated Material Cost:** $15-25 (depending on filament brand)

## General Printing Guidelines

### Recommended Settings

```
Printer Type: FDM (tested on Ender 3, Prusa i3)
Nozzle Size: 0.4mm
Print Speed: 50-60mm/s
Bed Temperature: 60°C (PLA), 80°C (PETG)
Nozzle Temperature: 200-210°C (PLA), 230-240°C (PETG)
Adhesion: Brim for tall parts, none for stable parts
```

### Material Recommendations

**PLA (Polylactic Acid):**
- Best for: Decorative parts, walls, tables, bar
- Pros: Easy to print, low warping, good detail
- Cons: Less heat resistant, more brittle
- Cost: ~$20/kg

**PETG (Polyethylene Terephthalate Glycol):**
- Best for: Motor mounts, DJ booth, structural parts
- Pros: Strong, heat resistant, flexible
- Cons: Stringing, slower print
- Cost: ~$25/kg

### Quality Tips

1. **Calibrate your printer** before starting (bed level, E-steps, flow rate)
2. **Print a test cube** with each new filament roll
3. **Use supports wisely** - only where necessary to save time/material
4. **Orient parts** with largest flat surface on build plate
5. **Enable "detect thin walls"** in slicer for detailed parts
6. **Dry your filament** if stored in humid conditions (60°C for 4-6 hours)

## Post-Processing

### Required Tools
- Craft knife or deburring tool
- Fine sandpaper (120, 220, 400 grit)
- Small files
- Super glue (cyanoacrylate) or plastic cement
- Primer and paint (optional)

### Steps

1. **Remove supports** carefully with pliers or flush cutters
2. **Clean up** edges and support marks with knife
3. **Sand** visible layer lines (start with 120 grit, finish with 400 grit)
4. **Test fit** all parts before gluing
5. **Glue assembly** following instructions in each PDF
6. **Paint** (optional) - use plastic primer first for best results

### Painting Tips (Optional)

For a more realistic finish:
- Prime with gray plastic primer spray
- Base coat with acrylic paint
- Detail painting (bar bottles, DJ equipment)
- Clear coat for protection

**Recommended colors:**
- DJ Booth: Black or dark gray
- Bar: Wood tone or metallic
- Tables: Black, white, or wood tone
- Walls: White or neutral gray

## Assembly Order

Follow this sequence for easiest assembly:

1. **Print all parts** (40-60 hours total)
2. **Post-process** (sanding, cleaning)
3. **Assemble DJ booth** and mount displays
4. **Build sliding wall mechanism** and install motors
5. **Construct bar counter**
6. **Assemble tables**
7. **Integrate electronics** (LEDs, wiring)
8. **Final decoration** and detailing

Detailed step-by-step instructions in each component's `assembly-instructions.pdf`.

## File Formats

Each model directory contains:
- **STL files** - Ready for slicing and printing
- **STEP files** - Source CAD for modifications (available on request)
- **Assembly PDFs** - Detailed instructions with photos

## Modifications

Want to customize the models?

### Using STEP Files

Import `.step` files into:
- **Fusion 360** (recommended, free for students)
- **FreeCAD** (free, open-source)
- **SolidWorks** (professional)
- **OnShape** (web-based, free)

### Common Modifications
- Resize for different scale clubs
- Add custom branding/logos
- Modify display cutouts for different screens
- Adapt motor mounts for different steppers

**Please share your modifications!** We'd love to see remixes.

## Troubleshooting

### Print Issues

**Warping corners:**
- Increase bed temperature (+5-10°C)
- Add brim or raft
- Use glue stick on bed
- Enclose printer to reduce drafts

**Supports not removing cleanly:**
- Reduce support density to 10-15%
- Increase support Z-distance to 0.2mm
- Use tree supports instead of linear
- Consider soluble supports (PVA)

**Layer adhesion problems:**
- Increase nozzle temperature (+5°C)
- Reduce print speed to 40mm/s
- Check for filament moisture
- Increase flow rate by 2-5%

**Stringing/oozing:**
- Enable retraction (5-6mm for Bowden, 1-2mm for direct drive)
- Reduce temperature by 5°C
- Increase retraction speed
- Enable "combing" mode

### Fit Issues

**Parts too tight:**
- Scale up slightly (101-102%)
- Sand contact surfaces
- Check printer dimensional accuracy

**Parts too loose:**
- Scale down slightly (98-99%)
- Add thin layer of glue
- Design tolerance was 0.2mm - adjust if needed

## Support & Questions

Having trouble with the 3D models?

1. Check the `assembly-instructions.pdf` in each directory
2. Review troubleshooting section above
3. Open an issue on GitHub with:
   - Photo of the problem
   - Your printer model
   - Slicer settings used
   - Filament brand/type

## Credits

**CAD Design:** Kire Angelov  
**Gear System Design:** Filip Mihailov, Kire Angelov  
**Original Club Architecture:** Gradezna Struka, [DSU RCSOO Nikola Karev Strumica]  
**Testing & Iteration:** Kiril Cvetkov, Filip Mihailov, Kire Angelov, Andrej Trendov

## License

These 3D models are licensed under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

You are free to:
- **Share** - Copy and redistribute in any medium or format
- **Adapt** - Remix, transform, and build upon the material

Under these terms:
- **Attribution** - Credit the original designers
- **ShareAlike** - Distribute modifications under the same license
- **No additional restrictions** - No legal/technological measures that restrict others

Full license: https://creativecommons.org/licenses/by-sa/4.0/

---

*Happy printing! 🖨️*
