from flask import Blueprint, render_template

from werkzeug.exceptions import HTTPException, default_exceptions, _aborter

# implement 402 manually until and unless it becomes part of werkzeug
class PaymentRequired(HTTPException):
	code = 402
	description = 'Payment required'

default_exceptions[402] = PaymentRequired
_aborter.mapping[402] = PaymentRequired

status_pages = Blueprint(
	'status_pages',
	__name__,
	template_folder='templates',
	static_folder='static',
	static_url_path='/status_pages'
)

def status_page(status_code, data={}):
	status_message = status_code
	status_data = {}
	if isinstance(data, dict):
		if 'message' in data and data['message']:
			status_message = data['message']
			del data['message']
		if 0 < len(data):
			status_data = data
	return (
		render_template(
			'status_page.html',
			status_code=status_code,
			status_message=status_message,
			status_data=status_data,
		),
		status_code
	)

@status_pages.app_errorhandler(400)
@status_pages.app_errorhandler(401)
@status_pages.app_errorhandler(402)
@status_pages.app_errorhandler(403)
@status_pages.app_errorhandler(404)
@status_pages.app_errorhandler(405)
@status_pages.app_errorhandler(406)
@status_pages.app_errorhandler(408)
@status_pages.app_errorhandler(409)
@status_pages.app_errorhandler(410)
@status_pages.app_errorhandler(411)
@status_pages.app_errorhandler(412)
@status_pages.app_errorhandler(413)
@status_pages.app_errorhandler(414)
@status_pages.app_errorhandler(415)
@status_pages.app_errorhandler(416)
@status_pages.app_errorhandler(417)
@status_pages.app_errorhandler(428)
@status_pages.app_errorhandler(429)
@status_pages.app_errorhandler(431)
@status_pages.app_errorhandler(451)
@status_pages.app_errorhandler(500)
@status_pages.app_errorhandler(501)
@status_pages.app_errorhandler(502)
@status_pages.app_errorhandler(503)
def error_handler(e):
	return status_page(e.code, e.description)
