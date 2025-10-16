# 1. นำเข้า Flask และฟังก์ชันที่จำเป็น
from flask import Flask, render_template, request

# 2. สร้าง Web Application 
app = Flask(__name__)

# 3. กำหนดเส้นทางสำหรับหน้าแรกของเว็บ
@app.route('/')
def home():
    #อ่านไฟล์ index.html มาแสดงผล
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

# 4. กำหนดเส้นทางสำหรับรับข้อมูลและแสดงผล
@app.route('/predict', methods=['POST'])
def predict():
    # 1. คำนวณคะแนนความเครียด (Stress Score) ---
    pss_answers = [int(request.form[f'pss{i}']) for i in range(1, 11)]
    stress_score = sum(pss_answers)
    
    # แปลผลคะแนนความเครียด
    if stress_score <= 13:
        stress_label = "ความเครียดระดับต่ำ (Low Stress)"
    elif stress_score <= 26:
        stress_label = "ความเครียดระดับปานกลาง (Moderate Stress)"
    else:
        stress_label = "ความเครียดระดับสูง (High Perceived Stress)"

    # 2. คำนวณคะแนนความวิตกกังวล (Anxiety Score) ---
    gad_answers = [int(request.form[f'gad{i}']) for i in range(1, 8)]
    anxiety_score = sum(gad_answers)

    # แปลผลคะแนนความวิตกกังวล
    if anxiety_score <= 4:
        anxiety_label = "ไม่มีความวิตกกังวล หรือมีในระดับน้อยมาก (Minimal Anxiety)"
    elif anxiety_score <= 9:
        anxiety_label = "มีความวิตกกังวลระดับน้อย (Mild Anxiety)"
    elif anxiety_score <= 14:
        anxiety_label = "มีความวิตกกังวลระดับปานกลาง (Moderate Anxiety)"
    else:
        anxiety_label = "มีความวิตกกังวลระดับรุนแรง (Severe Anxiety)"

    # 3. คำนวณคะแนนภาวะซึมเศร้า (Depression Score) ---
    phq_answers = [int(request.form[f'phq{i}']) for i in range(1, 10)]
    depression_score = sum(phq_answers)

    # แปลผลคะแนนภาวะซึมเศร้า (โค้ดเดิม)
    if depression_score <= 4:
        depression_label = "ไม่มีภาวะซึมเศร้า หรือมีในระดับน้อยมาก (Minimal Depression)"
    elif depression_score <= 9:
        depression_label = "มีภาวะซึมเศร้าระดับน้อย (Mild Depression)"
    elif depression_score <= 14:
        depression_label = "มีภาวะซึมเศร้าระดับปานกลาง (Moderate Depression)"
    elif depression_score <= 19:
        depression_label = "มีภาวะซึมเศร้าระดับค่อนข้างรุนแรง (Moderately Severe Depression)"
    else:
        depression_label = "มีภาวะซึมเศร้าระดับรุนแรง (Severe Depression)"

    # ส่งผลลัพธ์ทั้งหมดไปที่หน้า result.html 
    return render_template('result.html',
                           stress_score=stress_score, stress_label=stress_label,
                           anxiety_score=anxiety_score, anxiety_label=anxiety_label,
                           depression_score=depression_score, depression_label=depression_label)
    
# ใช้ทำนายแนวโน้มจาก อายุ, เกรด และปีที่เรียน
@app.route('/predictor')
def predictor():
    return render_template('predictor.html')

@app.route('/run_prediction', methods=['POST'])
def run_prediction():
    # 1. รับค่าจากฟอร์ม
    age = int(request.form['age'])
    gpa = float(request.form['gpa'])
    year = int(request.form['year'])

    # 2. คำนวณคะแนนที่ทำนายตามสมการ Regression
    predicted_stress = 29.5 + (age * -0.28) + (gpa * -0.57) + (year * 0.52)
    predicted_anxiety = 15.0 + (age * -0.15) + (gpa * -0.2) + (year * 0.47)
    predicted_depression = 18.2 + (age * -0.2) + (gpa * -0.2) + (year * 0.47)

    # แปลผลคะแนนความเครียด
    if predicted_stress <= 13:
        stress_label = "แนวโน้มความเครียดระดับต่ำ"
    elif predicted_stress <= 26:
        stress_label = "แนวโน้มความเครียดระดับปานกลาง"
    else:
        stress_label = "แนวโน้มความเครียดระดับสูง"

    # แปลผลคะแนนความวิตกกังวล
    if predicted_anxiety <= 4:
        anxiety_label = "แนวโน้มความวิตกกังวลระดับน้อยมาก"
    elif predicted_anxiety <= 9:
        anxiety_label = "แนวโน้มความวิตกกังวลระดับน้อย"
    elif predicted_anxiety <= 14:
        anxiety_label = "แนวโน้มความวิตกกังวลระดับปานกลาง"
    else:
        anxiety_label = "แนวโน้มความวิตกกังวลระดับรุนแรง"

    # แปลผลคะแนนภาวะซึมเศร้า
    if predicted_depression <= 4:
        depression_label = "แนวโน้มภาวะซึมเศร้าระดับน้อยมาก"
    elif predicted_depression <= 9:
        depression_label = "แนวโน้มภาวะซึมเศร้าระดับน้อย"
    elif predicted_depression <= 14:
        depression_label = "แนวโน้มภาวะซ-ึมเศร้าระดับปานกลาง"
    elif predicted_depression <= 19:
        depression_label = "แนวโน้มภาวะซึมเศร้าระดับค่อนข้างรุนแรง"
    else:
        depression_label = "แนวโน้มภาวะซึมเศร้าระดับรุนแรง"
    
    # 4. ส่งผลลัพธ์ทั้งหมดไปแสดงที่หน้าใหม่
    return render_template('prediction_result.html',
                           stress_score=round(predicted_stress, 2),
                           anxiety_score=round(predicted_anxiety, 2),
                           depression_score=round(predicted_depression, 2),
                           stress_label=stress_label,
                           anxiety_label=anxiety_label,
                           depression_label=depression_label)
    
if __name__ == '__main__':
    app.run(debug=True)