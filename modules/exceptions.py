
from sanic import response
from sanic.exceptions import NotFound
from modules import app

@app.exception(NotFound)
async def ignore_404s(request, exception):
	return response.redirect('/')
