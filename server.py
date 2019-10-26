from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io._html as phtml

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
  return 'Click.' + phtml.to_html(fig, full_html=False)

if __name__ == '__main__':
  app.run(debug=True)

# fig
