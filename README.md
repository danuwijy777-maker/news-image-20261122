# news-image-20261122

> make.fun bounty entry — **"Sum up 22 November's world news in one image"**
> Entry by [@nonamee](https://make.fun/@nonamee)

## What it does

Generates a 1024 × 1024 PNG newspaper front-page (`entry.png`) summarising
the four biggest global stories of **Sunday, 22 November 2026**:

1. **COP31 Antalya** – ended without a deal (first failure since 2009), "fossil fuels" dropped from text, two-day overrun.
2. **Iran / Hormuz** – ~25 tankers struck since 14 Nov; Iran claims it shot down a US MQ-1 drone.
3. **Zelensky / Patriots** – Ukraine presses the US to release Patriot batteries from strategic reserve.
4. **World Chess** – Gukesh vs Sindarov championship opens in Geneva; Game 1 on 24 November.

## Requirements

- Python 3.9+
- [Pillow](https://pillow.readthedocs.io/) (`pip install Pillow`)

## Usage

```bash
# 1. Generate the image
python make_image.py

# 2. Run the entry (copies entry.png to MAKEFUN_OUTPUT_DIR)
MAKEFUN_OUTPUT_DIR=/path/to/output python main.py
```

## License

MIT – see [LICENSE](LICENSE).
