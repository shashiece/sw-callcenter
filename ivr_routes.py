from flask import render_template, url_for, flash, request, redirect, Response
from __main__ import app
from signalwire.voice_response import VoiceResponse, Say , Gather

@app.route('/welcome_ivr', methods=['GET','POST'])
def welcom_ivr():
    response = VoiceResponse()
    response.say('Welcome to Signalwire Support ')
    gather = Gather(action='/ivr_menu_1', method='POST')
    gather.say('If you want to speak with our support team please Press 1, if you waht If you want to speace with our sales team please press 2 or if you waht to record your queries please press 3')
    response.append(gather)
    response.say('We did not receive any input. Goodbye!')
    response.hangup()
    return Response(str(response), mimetype='text/xml')

@app.route('/ivr_menu_1', methods=['POST'])
def ivr_menu_1():
   response = VoiceResponse()
   digit = request.form['Digits']
   if digit == '1': # support queue
      response.play("https://vmrec01.signalwire.cloud/pleasehold.wav")
      response.enqueue('support')
   elif digit == '2': # Sales Queue
      response.play("https://vmrec01.signalwire.cloud/pleasehold.wav")
      response.enqueue('sales')
   elif digit == '3':
      response.say('Please leave a message at the beep. Press the pound key when finished.')
      response.record(action='/record_action', method='POST', max_length=15, finish_on_key='#')
   else:
      response.hangup()
   return Response(str(response), mimetype='text/xml') 

