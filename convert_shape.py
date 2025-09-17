import os
import shutil

def convert_dataset(src_dir, dst_dir):
    """
    Convert dataset structure từ Roboflow format sang YOLO chuẩn:
    
    Input (Roboflow):
        src_dir/
            train/images/
            train/labels/
            valid/images/
            valid/labels/
            test/images/ (tùy chọn)
            test/labels/ (tùy chọn)

    Output (YOLO chuẩn):
        dst_dir/
            images/train/
            images/val/
            images/test/
            labels/train/
            labels/val/
            labels/test/
            data.yaml (copy từ src_dir nếu có)
    """

    # Danh sách split cần xử lý
    splits = ["train", "valid", "test"]

    for split in splits:
        img_src = os.path.join(src_dir, split, "images")
        lbl_src = os.path.join(src_dir, split, "labels")

        # Nếu thư mục không tồn tại thì bỏ qua (VD: test có thể không có)
        if not os.path.exists(img_src) or not os.path.exists(lbl_src):
            continue

        # Roboflow dùng "valid", YOLO chuẩn dùng "val"
        split_name = "val" if split == "valid" else split

        img_dst = os.path.join(dst_dir, "images", split_name)
        lbl_dst = os.path.join(dst_dir, "labels", split_name)

        os.makedirs(img_dst, exist_ok=True)
        os.makedirs(lbl_dst, exist_ok=True)

        # Copy ảnh
        for f in os.listdir(img_src):
            shutil.copy(os.path.join(img_src, f), os.path.join(img_dst, f))

        # Copy nhãn
        for f in os.listdir(lbl_src):
            shutil.copy(os.path.join(lbl_src, f), os.path.join(lbl_dst, f))

    # Copy data.yaml nếu có
    yaml_src = os.path.join(src_dir, "data.yaml")
    if os.path.exists(yaml_src):
        shutil.copy(yaml_src, os.path.join(dst_dir, "data.yaml"))

    print(f"✅ Done! Dataset đã convert sang {dst_dir}")


if __name__ == "__main__":
    src = "Fruit Dataset.v1i.yolov11"
    dst = "FruitDataset_converted"
    convert_dataset(src, dst)
