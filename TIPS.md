# 使用技巧 (Usage Tips)

## 常见使用模式

### 1. 公众号文章工作流

#### 步骤1: 收集素材PDF
将需要的PDF文档放到一个文件夹：
```bash
mkdir wechat_materials
cp ~/Documents/*.pdf wechat_materials/
```

#### 步骤2: 批量提取
```bash
cd wechat_materials
for pdf in *.pdf; do
    python /path/to/pdf_to_image.py "$pdf" -e -o "../wechat_images"
done
```

#### 步骤3: 筛选和使用
在 `wechat_images/` 文件夹中筛选需要的图片，直接上传到公众号编辑器。

### 2. 命令别名设置

添加到你的 `.bashrc` 或 `.zshrc`：
```bash
alias pdf2img='python /path/to/pdf_to_image.py'
alias pdfext='python /path/to/pdf_to_image.py -e'
```

使用：
```bash
pdf2img document.pdf -p 1 3 5
pdfext document.pdf
```

### 3. 与其他工具组合

#### 配合图片压缩工具
```bash
# 转换后压缩
python pdf_to_image.py doc.pdf
optipng output/*.png  # 或使用 ImageOptim (macOS)
```

#### 配合图片编辑
```bash
# 转换为JPEG，然后批量编辑
python pdf_to_image.py doc.pdf -f jpg
# 使用 ImageMagick 添加水印
mogrify -gravity SouthEast -pointsize 20 -draw "text 10,10 '@MyBlog'" output/*.jpg
```

### 4. Python脚本集成示例

#### 自动化处理脚本
```python
#!/usr/bin/env python3
"""自动处理PDF并上传到云存储"""

import os
from pdf_to_image import PDFImageConverter
from pathlib import Path

def process_and_organize(pdf_path, output_base="processed"):
    """处理PDF并按日期组织"""
    from datetime import datetime
    
    # 创建日期文件夹
    date_str = datetime.now().strftime("%Y%m%d")
    output_dir = Path(output_base) / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with PDFImageConverter(pdf_path) as converter:
        # 转换前5页
        pages = converter.convert_pages_to_images(
            output_dir=str(output_dir),
            pages=list(range(1, min(6, converter.page_count + 1))),
            dpi=300
        )
        
        # 提取所有图片
        extracted = converter.extract_images(
            output_dir=str(output_dir)
        )
        
        print(f"✓ {len(pages)} pages + {len(extracted)} images → {output_dir}")
        return output_dir

# 使用
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = process_and_organize(sys.argv[1])
        print(f"All done! Check: {result}")
```

### 5. 质量优化技巧

#### 超高清输出（印刷品质）
```bash
python pdf_to_image.py document.pdf -d 600 -f png
```

#### Web优化（快速加载）
```bash
python pdf_to_image.py document.pdf -d 150 -f jpg
```

#### 移动端优化
```bash
# 较低DPI，JPEG格式，文件更小
python pdf_to_image.py document.pdf -d 120 -f jpg
```

### 6. 特殊场景处理

#### 处理超大PDF（100+页）
```bash
# 分批处理，注意页码是空格分隔的
python pdf_to_image.py large.pdf -p 1 2 3 4 5 -o batch1
python pdf_to_image.py large.pdf -p 6 7 8 9 10 -o batch2
# ... 依此类推
```

#### 只提取大图（过滤小图标）
```bash
# 只提取宽度和高度都大于500px的图片
python pdf_to_image.py document.pdf -e --min-width 500 --min-height 500
```

#### 保留文件名规则
使用脚本重命名：
```python
import os
import re
from pathlib import Path

def rename_with_date(folder):
    """给文件名添加日期前缀"""
    from datetime import datetime
    prefix = datetime.now().strftime("%Y%m%d_")
    
    for file in Path(folder).glob("*.png"):
        new_name = file.parent / (prefix + file.name)
        file.rename(new_name)
        print(f"Renamed: {file.name} → {new_name.name}")

rename_with_date("output")
```

## Claude Code 集成示例

### 示例1: 让Claude帮你批量处理
对Claude说：
```
请帮我写一个脚本，批量处理当前目录下的所有PDF文件，
提取每个PDF的前3页和所有嵌入图片，保存到以PDF文件名命名的文件夹中
```

### 示例2: 自定义处理逻辑
对Claude说：
```
请帮我修改pdf_to_image.py，添加一个功能：
在转换时自动裁剪掉页边距，只保留内容区域
```

### 示例3: 集成到工作流
对Claude说：
```
请帮我写一个Python脚本，实现以下工作流：
1. 从PDF提取图片
2. 压缩图片大小
3. 添加水印
4. 上传到七牛云/阿里云OSS
5. 返回图片URL列表
```

## 常见问题解决

### Q: ModuleNotFoundError: No module named 'fitz'
```bash
pip install PyMuPDF
```

### Q: 转换的图片太大
```bash
# 降低DPI或使用JPEG
python pdf_to_image.py doc.pdf -d 150 -f jpg
```

### Q: 提取不到图片
可能PDF中的图片是内嵌在矢量图形中的，尝试转换页面：
```bash
python pdf_to_image.py doc.pdf -p <页码>
```

### Q: 处理速度慢
- 只处理需要的页面（使用 `-p`）
- 降低DPI（使用 `-d 150`）
- 使用多进程（参考 `examples.py`）

### Q: 某些PDF无法处理
- 检查PDF是否加密（需要先解密）
- 检查PDF是否损坏（尝试用PDF阅读器打开）
- 更新依赖：`pip install --upgrade PyMuPDF`

## 性能优化建议

### 1. 合理选择DPI
- 150 DPI: 网页展示
- 300 DPI: 公众号/标准打印（推荐）
- 600 DPI: 高品质印刷

### 2. 合理选择格式
- PNG: 文字、图表、需要透明度
- JPEG: 照片、不需要透明度、需要小文件

### 3. 批量处理优化
```bash
# 使用通配符批量处理
for f in reports/*.pdf; do 
    python pdf_to_image.py "$f" -e -o "images/$(basename $f .pdf)"
done
```

## 进阶使用

### 自定义输出文件名
修改代码或使用脚本后处理：
```python
from pdf_to_image import PDFImageConverter
import os

with PDFImageConverter("doc.pdf") as converter:
    paths = converter.convert_pages_to_images(output_dir="temp")
    
    # 重命名为自定义格式
    for i, path in enumerate(paths, 1):
        new_name = f"custom_name_{i:03d}.png"
        os.rename(path, os.path.join("output", new_name))
```

### 添加自定义处理
```python
from pdf_to_image import PDFImageConverter
from PIL import Image, ImageEnhance

with PDFImageConverter("doc.pdf") as converter:
    paths = converter.convert_pages_to_images(output_dir="temp")
    
    # 后处理：增强对比度
    for path in paths:
        img = Image.open(path)
        enhancer = ImageEnhance.Contrast(img)
        enhanced = enhancer.enhance(1.5)
        enhanced.save(path.replace("temp", "enhanced"))
```

## 获取帮助

- 查看帮助：`python pdf_to_image.py --help`
- 查看示例：查看 `examples.py`
- 查看文档：查看 `README.md` 和 `QUICKSTART.md`
- 报告问题：在GitHub上提Issue

---

**提示**: 保存常用命令为shell脚本或Python脚本，可以大大提高效率！
