from flask import Flask, render_template, request, jsonify
from utils import extract_text_from_pdf, calculate_score

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    files = request.files.getlist('resumes')
    jd = request.form['jd']
    
    results = []

    for file in files:
        if file.filename == '':
            continue
            
        resume_text = extract_text_from_pdf(file)
        score, matched, missing = calculate_score(resume_text, jd)
        
        # Keep all results so the user can see exactly what score each resume received
        results.append({
            "filename": file.filename,
            "score": score,
            "matched": matched,
            "missing": missing
        })
            
    # Sort results by score descending
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)