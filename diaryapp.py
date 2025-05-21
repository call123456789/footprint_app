from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QSize
import os, json
import shutil

class DiaryApp(QWidget):
    def __init__(self, dir, parent):
        super().__init__(parent=parent)
        self.initUI()
        self.dir = dir
        self.image_paths = []
        self.parent = parent
        if os.path.exists(self.dir):
            self.load_existing_data()  # 初始化时自动加载已有数据

    def load_existing_data(self):
        """加载已存在的日记数据"""
        json_path = os.path.join(self.dir, "info.json")
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                metadata = json.load(f)
                
            # 填充文本字段
            self.time_input.setText(metadata.get("time", ""))
            self.location_input.setText(metadata.get("location", ""))
            self.content_input.setPlainText(metadata.get("content", ""))
                
            # 加载图片
            for img_path in metadata.get("images", []):
                if os.path.exists(img_path):
                    self.image_paths.append(img_path)
                    item = QListWidgetItem(QIcon(img_path), os.path.basename(img_path))
                    self.image_list.addItem(item)

    def initUI(self):
        # 主布局
        main_layout = QVBoxLayout()

        # 输入区域
        form_layout = QFormLayout()
        self.time_input = QLineEdit()
        self.time_input.setFixedWidth(500)
        self.location_input = QLineEdit()
        self.location_input.setFixedWidth(500)
        self.content_input = QTextEdit()
        self.content_input.setFixedWidth(700)
        form_layout.addRow("时间(必填)：", self.time_input)
        form_layout.addRow("地点(必填)：", self.location_input)
        form_layout.addRow("日记：", self.content_input)

        # 图片区域
        img_group = QGroupBox("图片(双击查看原图)")
        img_layout = QHBoxLayout()
        
        self.image_list = QListWidget()
        self.image_list.setIconSize(QSize(100, 100))
        self.image_list.itemDoubleClicked.connect(self.show_full_image)
        
        # 图片操作按钮
        btn_layout = QVBoxLayout()
        upload_btn = QPushButton("上传图片")
        upload_btn.clicked.connect(self.upload_image)
        delete_btn = QPushButton("删除选中")
        delete_btn.clicked.connect(self.delete_image)
        btn_layout.addWidget(upload_btn)
        btn_layout.addWidget(delete_btn)
        
        img_layout.addWidget(self.image_list)
        img_layout.addLayout(btn_layout)
        img_group.setLayout(img_layout)

        # 组合布局
        main_layout.addLayout(form_layout)
        main_layout.addWidget(img_group)

        self.setLayout(main_layout)
        self.resize(800, 600)

    def upload_image(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "Images (*.png *.jpg *.jpeg)")
        for file in files:
            self.image_paths.append(file)
            item = QListWidgetItem(QIcon(file), os.path.basename(file))
            self.image_list.addItem(item)

    def delete_image(self):
        selected_indices = sorted(
            [self.image_list.row(item) for item in self.image_list.selectedItems()],
            reverse=True
        )
        
        for index in selected_indices:
            # 获取文件路径并删除本地文件
            file_path = self.image_paths[index]
            if os.path.exists(file_path):
                os.remove(file_path)
                
            # 移除列表项和路径记录
            self.image_list.takeItem(index)
            del self.image_paths[index]

    def show_full_image(self, item):
        dialog = QDialog()
        dialog.setWindowTitle("查看大图")
        label = QLabel()
        pixmap = QPixmap(item.text())
        label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        scroll = QScrollArea()
        scroll.setWidget(label)
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_diary(self):
        # 校验输入
        time = self.time_input.text().strip()
        location = self.location_input.text().strip()
        
        if not time or not location:
            QMessageBox.warning(self, "输入不完整", "请填写时间和地点后再保存！")
            return

        # 创建存储目录
        
        os.makedirs(self.dir, exist_ok=True)

        self.parent.upd_turn()

        # 保存图片
        saved_images = []
        for path in self.image_paths:
            dest = os.path.join(self.dir, os.path.basename(path))
            # 路径相同性检查
            if os.path.abspath(path) == os.path.abspath(dest):
                saved_images.append(dest)  # 直接使用已有文件
                continue

            shutil.copy2(path, dest)
            saved_images.append(dest)

        # 保存元数据
        metadata = {
            "time": self.time_input.text(),
            "location": self.location_input.text(),
            "content": self.content_input.toPlainText(),
            "images": saved_images
        }
        with open(os.path.join(self.dir, "info.json"), "w") as f:
            json.dump(metadata, f, ensure_ascii=False)

