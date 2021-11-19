from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def web():
    if request.method == 'GET':
        return render_template('web.html')

    if request.method == "POST":
        file_name = request.form['timelogfile']
        try:
            with open(file_name, 'r') as timelog_file:
              Line_Num = 0
              Total_Perfect_lines = 0
              Error_lines = 0
              total_consumed_time = 0
              for line in timelog_file:
                 Line_Num += 1
                 if line.find("Time Log:") == 0:
                    continue
                 if 'am' not in line.lower() and 'pm' not in line.lower():
                     Error_lines +=1
                     continue
                 Total_Perfect_lines +=1
                 begin_time = datetime.strptime(line.split('-')[0].strip()[-7:].lower().strip(), '%I:%M%p')
                 end_time = datetime.strptime(line.split('-')[1][1:8].lower().strip(), '%I:%M%p')
                 consumed_time = end_time - begin_time
                 total_consumed_time = total_consumed_time+(consumed_time.seconds/60)
               
                 return render_template('web.html',
                                    file_name = file_name.split('.')[0],
                                    Total_Perfect_lines= Total_Perfect_lines,
                                    Error_lines= Error_lines,
                                    result='{:02d} hours {:02d} minutes'.format(*divmod(int(total_consumed_time), 60)))
        except FileNotFoundError:
            error = "Please Choose the data file in DropDown"
            return render_template('web.html', error_File_Notfound = error)

if __name__ == '__main__':
    app.run(debug=True)
