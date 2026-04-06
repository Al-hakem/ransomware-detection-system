# ================================
# استدعاء المكتبات
# ================================

import os                 # للتعامل مع الملفات والفولدرات
import pefile             # لتحليل ملفات PE
import pandas as pd       # لإنشاء جدول البيانات
import math               # entropy لحساب اللوغاريتم في 
import hashlib            # SHA256 لحساب 


# ================================
# إعداد المسارات
# ================================

dataset_path = "dataset"
output_file = "pe_features.csv"

data = []


# ================================
# Shannon Entropy دالة حساب 
# ================================

def calculate_entropy(byte_data):
    """
    بتحسب درجة العشوائية في البيانات.
    كل ما الرقم يزيد → البيانات أقرب لتشفير.
    """
    if not byte_data:
        return 0

    entropy = 0
    length = len(byte_data)

    for x in range(256):
        p_x = byte_data.count(bytes([x])) / length
        if p_x > 0:
            entropy -= p_x * math.log2(p_x)

    return entropy


# ================================
# SHA256 دالة حساب 
# ================================

def calculate_sha256(file_path):
    """
    SHA256 هو بصمة رقمية فريدة لكل ملف.
    مهم جدًا في أبحاث المالوير لتتبع العينات.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


# ================================
# نبدأ قراءة الملفات
# ================================

for label in ["benign", "ransomware"]:

    folder_path = os.path.join(dataset_path, label)

    for file_name in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file_name)

        try:
            pe = pefile.PE(file_path)

            # ----------------------------
            # معلومات عامة عن الملف
            # ----------------------------

            sha256 = calculate_sha256(file_path)  # بصمة الملف

            num_sections = len(pe.sections)       # عدد الـ sections
            size_of_image = pe.OPTIONAL_HEADER.SizeOfImage
            size_of_code = pe.OPTIONAL_HEADER.SizeOfCode
            entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint

            # ----------------------------
            # حساب Imports
            # ----------------------------

            num_imports = 0
            num_dlls = 0

            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                num_dlls = len(pe.DIRECTORY_ENTRY_IMPORT)
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    num_imports += len(entry.imports)

            # ----------------------------
            # حساب Entropy لكل Section
            # ----------------------------

            section_entropies = []

            for section in pe.sections:
                section_data = section.get_data()
                entropy = calculate_entropy(section_data)
                section_entropies.append(entropy)

            # متوسط entropy
            avg_entropy = sum(section_entropies) / len(section_entropies) if section_entropies else 0

            # أعلى entropy
            max_entropy = max(section_entropies) if section_entropies else 0

            # أقل entropy
            min_entropy = min(section_entropies) if section_entropies else 0

            # ----------------------------
            # إضافة البيانات للجدول
            # ----------------------------

            data.append([
                sha256,
                file_name,
                num_sections,
                size_of_image,
                size_of_code,
                entry_point,
                num_imports,
                num_dlls,
                avg_entropy,
                max_entropy,
                min_entropy,
                0 if label == "benign" else 1
            ])

        except Exception as e:
            print(f"Error processing {file_name}: {e}")


# ================================
# إنشاء DataFrame
# ================================

columns = [
    "sha256",
    "file_name",
    "num_sections",
    "size_of_image",
    "size_of_code",
    "entry_point",
    "num_imports",
    "num_dlls",
    "avg_entropy",
    "max_entropy",
    "min_entropy",
    "label"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv(output_file, index=False)

print("Feature extraction completed successfully.")
