from flask import Flask, render_template
import plotly.graph_objects as go

fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
# fig.show()
# fig.write_html('first_figure.html', auto_open=True)

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/my-link/')
def my_link():
  print('I got clicked!')
  fig.write_html('my_html.html')
  return 'Click.' + send_from_directory('my_html.html')

if __name__ == '__main__':
  app.run(debug=True)

# fig
