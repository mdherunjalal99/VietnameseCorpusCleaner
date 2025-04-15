from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import tempfile
import logging
from werkzeug.utils import secure_filename
from vietnamese_corpus_filter import filter_corpus

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Đường dẫn thư mục tạm thời để lưu trữ tệp
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Kiểm tra xem có file được gửi lên không
    if 'file' not in request.files:
        flash('Không có file nào được chọn')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Nếu người dùng không chọn file hoặc tên file rỗng
    if file.filename == '':
        flash('Không có file nào được chọn')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Lưu file đầu vào
        file.save(input_path)
        
        # Tạo tên file đầu ra
        output_filename = f"{os.path.splitext(filename)[0]}_filtered.txt"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        try:
            # Thực hiện lọc corpus
            filter_corpus(input_path, output_path)
            
            # Trả về file đã lọc cho người dùng
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            logger.error(f"Lỗi khi xử lý file: {str(e)}")
            flash(f'Có lỗi xảy ra khi xử lý file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Chỉ cho phép tải lên file .txt')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)