from flask import Blueprint
from flask.templating import render_template
from flaskblog.machine.forms import SentimentForm, SummarizeForm
from flaskblog.machine.utils import summmarize, sentiment_analysis
machine = Blueprint('machine', __name__)

@machine.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    form = SentimentForm()
    if form.validate_on_submit():
        text = form.text.data
        result, per = sentiment_analysis(text)
        form.result.data = result
        form.per.data = per
        return render_template('sentiment.html', title='Sentiment Analysis', form=form, legend='Sentiment Analysis')
    else:
        return render_template('sentiment.html', title='Sentiment Analysis', form=form, legend='Sentiment Analysis')


@machine.route('/textsummarizer', methods=['GET', 'POST'])
def summarizer():
    form = SummarizeForm()
    if form.validate_on_submit():
        text = form.text.data
        num = form.num.data
        summary = summmarize(text, num)
        form.summary.data = summary
        return render_template('summarizer.html', title='Text Summarizer', form=form, legend='Text Summarizer')
    else:
        return render_template('summarizer.html', title='Text Summarier', form=form, legend='Text Summarizer')