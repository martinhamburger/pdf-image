# 快速开始指南

## 5分钟上手 PDF to Image

### 1. 安装（30秒）

```bash
pip install PyMuPDF Pillow
```

### 2. 最简单用法（30秒）

```bash
# 下载代码
git clone https://github.com/martinhamburger/pdf-image.git
cd pdf-image

# 转换PDF
python pdf_to_image.py your_document.pdf
```

就这么简单！图片已经保存在 `output/` 文件夹中。

### 3. 常用命令

```bash
# 提取PDF中的所有图片
python pdf_to_image.py document.pdf -e

# 只转换第1页
python pdf_to_image.py document.pdf -p 1

# 转换为JPEG格式
python pdf_to_image.py document.pdf -f jpg

# 查看PDF有多少页
python pdf_to_image.py document.pdf -i
```

### 4. 公众号使用场景

#### 场景A: 从技术文档提取图表
```bash
# 假设图表在第5、10、15页
python pdf_to_image.py tech_doc.pdf -p 5 10 15 -o wechat_images
```

#### 场景B: 提取论文中的所有图片
```bash
# 提取所有嵌入图片（通常质量最好）
python pdf_to_image.py paper.pdf -e -o paper_figures
```

#### 场景C: 制作封面图
```bash
# 只转换第一页，高质量PNG
python pdf_to_image.py document.pdf -p 1 -d 300 -f png
```

### 5. 在代码中使用

```python
from pdf_to_image import PDFImageConverter

# 三行代码搞定
with PDFImageConverter("document.pdf") as converter:
    images = converter.convert_pages_to_images()
    extracted = converter.extract_images()
```

### 6. 常见问题

**Q: 图片模糊怎么办？**  
A: 使用更高的DPI: `python pdf_to_image.py doc.pdf -d 400`

**Q: 文件太大怎么办？**  
A: 使用JPEG格式或降低DPI: `python pdf_to_image.py doc.pdf -f jpg -d 150`

**Q: 只需要某几页？**  
A: 使用 `-p` 参数: `python pdf_to_image.py doc.pdf -p 1 3 5`

### 7. 下一步

- 查看 [README.md](README.md) 了解所有功能
- 查看 [examples.py](examples.py) 学习高级用法
- 开始处理你的PDF文件！

---

**提示**: 第一次使用时，建议先用 `-i` 参数查看PDF信息，了解PDF有多少页、每页有多少图片。

```bash
python pdf_to_image.py your_document.pdf -i
```
