#!/bin/sh
# Renders a LinkedIn carousel folder with headless Chrome.
#   slide-N.html -> <name>-N.png at 2160 x 2700 (a slide marked data-photo becomes <name>-N.jpg)
#   all <name>-N.png|jpg in the folder, in order -> <name>-carousel.pdf, 1080 x 1350 px pages
# Usage: sh render.sh <carousel-folder> <name>
set -e
DIR="$(cd "$1" && pwd)"
NAME="$2"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE" "$DIR/.pdf.html"' EXIT

for html in "$DIR"/slide-*.html; do
  [ -e "$html" ] || continue
  n=$(basename "$html" .html | sed 's/^slide-//')
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$PROFILE" \
    --force-device-scale-factor=2 --window-size=1080,1350 --virtual-time-budget=3000 \
    --screenshot="$DIR/$NAME-$n.png" "file://$html" >/dev/null 2>&1
  if grep -q 'data-photo' "$html"; then
    sips -s format jpeg -s formatOptions 88 "$DIR/$NAME-$n.png" --out "$DIR/$NAME-$n.jpg" >/dev/null
    rm "$DIR/$NAME-$n.png"
  fi
done

pages=""
for img in $(ls "$DIR" | grep -E "^$NAME-[0-9]+\.(png|jpg)$" | sort); do
  pages="$pages<div class=\"page\"><img src=\"$img\"></div>"
done
cat > "$DIR/.pdf.html" <<EOF
<!doctype html><html><head><meta charset="utf-8"><style>
@page{size:810pt 1012.5pt;margin:0}
html,body{margin:0;padding:0}
.page{width:100vw;height:100vh;overflow:hidden}
.page+.page{break-before:page}
.page img{display:block;width:100%;height:100%;object-fit:cover}
</style></head><body>$pages</body></html>
EOF
"$CHROME" --headless=new --disable-gpu --user-data-dir="$PROFILE" --no-pdf-header-footer \
  --virtual-time-budget=3000 --print-to-pdf="$DIR/$NAME-carousel.pdf" "file://$DIR/.pdf.html" >/dev/null 2>&1
ls "$DIR" | grep -E "^$NAME-"
