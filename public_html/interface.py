from flask import Flask, render_template, request, redirect
from subprocess import check_output
import os 
app = Flask(__name__)



def generate_uniquegroups():

	#UNCOMMENT THIS TO RUN config.json related commands
	#subprocess.call(['grep -o -P '(?<=group-title=").*(?=")' <M3U FILE/output> | sort | uniq | tr A-Z a-z | sed -r s/$/\",/ | sed -r s/^/\"/ > uniquegroups.txt'])
	
	fname = 'uniquegroups.txt'
	with open(fname) as f:
	    content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content]
	return content 



def delete_lines(line):
    to_delete = line
    fname = 'uniquegroups.txt'
    with open(fname, "r") as f:
        lines = f.readlines()


    with open(fname, "w") as f:
         for line in lines:
            if line.strip("\n") != to_delete:
                f.write(line)
    print("Delete succesful!")


def construct_config():
	#this removes the final comma to provide valid json
	subprocess.call(["sed -i '$ s/.$//' uniquegroups.txt"])

	# this removes the existing groups from the json
	subprocess.call(["sed -i '/\"groups\"\: \[/,/],/{//!d}' config.json"])

	# this imports the groups into json.
	subprocess.call(["sed -i -e '/\"groucd s\"\: \[/,/],/{//!d}' -e '/\"groups\"\: \[/r uniq.txt' config.json"])

	subprocess.call(["sed -i -e '/\"groucd s\"\: \[/,/],/{//!d}' -e '/\"groups\"\: \[/r uniq.txt' config.json"])

	#run 
	os.system('python m3u-epg-editor.py -j config.json')

@app.route("/", methods=['GET', 'POST'])
def m3u():

    lines = generate_uniquegroups()

    count = list(range(0,len(lines)))
    print(str(count))


    if request.method == 'POST':
        items = request.form.getlist('m3u')
        print(str(items))
        items = [str(r) for r in items]
        lines = [str(r) for r in lines]

        items = [x for x in lines if x not in items]
        items = [x for x in items if x]
        print(str(items))
        for item in items:
            delete_lines(item)



        #UNCOMMENT THIS TO RUN config.json related commands
        #construct_config()

        return redirect('/')





    return render_template("main.html", data=zip(lines,count))

if __name__ == "__main__":
	app.run()