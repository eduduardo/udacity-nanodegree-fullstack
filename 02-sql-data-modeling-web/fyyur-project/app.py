#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import *
from config import *
from datetime import datetime
import sys

#----------------------------------------------------------------------------#
# Filters
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value)) # forcing convert to string before parse to avoid an error
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Venues
#----------------------------------------------------------------------------#
@app.route('/venues')
def venues():
  # first grouping by city and state of all venues avaliables
  groups_city_and_state = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).order_by(Venue.state)

  areas = []

  # looping through all city and states for get individual venues attributes
  for city, state in groups_city_and_state:
      venues_filtered = Venue.query.filter_by(city=city,state=state).all()

      venues = []

      for venue in venues_filtered:
          num_upcoming_shows = venue.artists.filter(Show.start_time > datetime.now()).count()

          venues.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
          })

      areas.append({
        "city": city,
        "state": state,
        "venues": venues
      })

  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')

  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # using ilike: https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.PropComparator.ilike
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()

  for venue in venues:
      venue.num_upcoming_shows = venue.artists.filter(Show.start_time > datetime.now()).count()

  results = {
    "count": len(venues),
    "data": venues
  }
  return render_template('pages/search_venues.html', results=results, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  if venue == None:
      abort(404)

  # converting back separating genres with the comma
  venue.genres = venue.genres.split(",")

  # source: https://stackoverflow.com/questions/17868743/doing-datetime-comparisons-in-filter-sqlalchemy
  upcoming_shows_all = venue.artists.filter(Show.start_time > datetime.now()).all()

  upcoming_shows = []
  for show in upcoming_shows_all:
      upcoming_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })

  past_shows_all = venue.artists.filter(Show.start_time < datetime.now()).all()

  past_shows = []
  for show in past_shows_all:
      past_shows.append({
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })

  venue.upcoming_shows = upcoming_shows
  venue.past_shows = past_shows
  venue.upcoming_shows_count = len(venue.upcoming_shows)
  venue.past_shows_count = len(venue.past_shows)

  return render_template('pages/show_venue.html', venue=venue)

#----------------------------------------------------------------------------#
# Create Venue
#----------------------------------------------------------------------------#
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  body = {}
  try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone', None)
      image_link = request.form.get('image_link')

      # using getlist to get all multiple select fields
      # source https://stackoverflow.com/a/12502681
      genres = request.form.getlist('genres')
      facebook_link = request.form.get('facebook_link', None)
      website = request.form.get('website', None)
      seeking_talent = bool(request.form.get('seeking_talent', False))
      seeking_description = request.form.get('seeking_description', None)

      # concatened genres list into string separated with ","
      genres = ','.join(genres)

      venue = Venue(name=name,city=city,state=state,address=address,phone=phone,
                   genres=genres,image_link=image_link,facebook_link=facebook_link,
                   website=website,seeking_talent=seeking_talent,seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()
      body['name'] = venue.name
  except:
      error=True
      body['name'] = request.form.get('name')
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
      flash('An error occurred. Venue ' + body['name'] + ' could not be listed.')
  else:
      flash('Venue ' + body['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Delete Venue
#----------------------------------------------------------------------------#
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  venue_name = ""
  try:
      venue_name = Venue.query.get(venue_id).name
      Venue.query.filter_by(id=venue_id).delete()
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
    flash('An error occurred. Venue ' + venue_name + ' could not be deleted.')
  else:
    flash('Venue ' + venue_name + ' was successfully deleted!')

  return redirect(url_for('index'), code=200)

#----------------------------------------------------------------------------#
# Edit Venue
#----------------------------------------------------------------------------#
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  if venue == None:
      abort(404)

  venue.genres = venue.genres.split(',')

  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone', None)
      image_link = request.form.get('image_link')
      genres = request.form.getlist('genres')
      facebook_link = request.form.get('facebook_link', None)
      website = request.form.get('website', None)
      seeking_talent = bool(request.form.get('seeking_talent', False))
      seeking_description = request.form.get('seeking_description', None)

      # concatened genres list into string separated with ","
      genres = ','.join(genres)

      venue = Venue.query.get(venue_id)
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone
      venue.genres = genres
      venue.image_link = image_link
      venue.facebook_link = facebook_link
      venue.website = website
      venue.seeking_talent = seeking_talent
      venue.seeking_description = seeking_description

      db.session.commit()
  except:
      error=True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
      flash('An error occurred. Venue could not be updated.')
  else:
      flash('Venue was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#----------------------------------------------------------------------------#
# Artists
#----------------------------------------------------------------------------#
@app.route('/artists')
def artists():
  artists = Artist.query.order_by(Artist.id).all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()

  for artist in artists:
      artist.num_upcoming_shows = artists.venues.filter(Show.start_time > datetime.now()).count()

  results = {
    "count": len(venues),
    "data": venues
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if artist == None:
      abort(404)

  # converting back separating genres with the comma
  artist.genres = artist.genres.split(",")

  upcoming_shows_all = artist.venues.filter(Show.start_time > datetime.now()).all()

  upcoming_shows = []
  for show in upcoming_shows_all:
      upcoming_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      })

  past_shows_all = artist.venues.filter(Show.start_time < datetime.now()).all()

  past_shows = []
  for show in past_shows_all:
      past_shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      })

  artist.upcoming_shows = upcoming_shows
  artist.past_shows = past_shows
  artist.upcoming_shows_count = len(artist.upcoming_shows)
  artist.past_shows_count = len(artist.past_shows)

  return render_template('pages/show_artist.html', artist=artist)

#----------------------------------------------------------------------------#
# Create Artists
#----------------------------------------------------------------------------#
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  body = {}
  try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone', None)
      image_link = request.form.get('image_link')

      genres = request.form.getlist('genres')
      facebook_link = request.form.get('facebook_link', None)
      website = request.form.get('website', None)
      seeking_venue = bool(request.form.get('seeking_venue', False))
      seeking_description = request.form.get('seeking_description', None)

      # concatened genres list into string separated with ","
      genres = ','.join(genres)

      artist = Artist(
        name=name,
        city=city,
        state=state,
        phone=phone,
        genres=genres,
        image_link=image_link,
        facebook_link=facebook_link,
        website=website,
        seeking_venue=seeking_venue,
        seeking_description=seeking_description
      )
      db.session.add(artist)
      db.session.commit()
      body['name'] = artist.name
  except:
      error=True
      body['name'] = request.form.get('name')
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
      flash('An error occurred. Artist ' + body['name'] + ' could not be listed.')
  else:
      flash('Artist ' + body['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Edit Artists
#----------------------------------------------------------------------------#
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if artist == None:
     abort(404)

  artist.genres = artist.genres.split(',')

  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone', None)
      image_link = request.form.get('image_link')
      genres = request.form.getlist('genres')
      facebook_link = request.form.get('facebook_link', None)
      website = request.form.get('website', None)
      seeking_venue = bool(request.form.get('seeking_venue', False))
      seeking_description = request.form.get('seeking_description', None)

      # concatened genres list into string separated with ","
      genres = ','.join(genres)

      artist = Artist.query.get(artist_id)
      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.genres = genres
      artist.image_link = image_link
      artist.facebook_link = facebook_link
      artist.website = website
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description

      db.session.commit()
  except:
      error=True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
      flash('An error occurred. Artist could not be updated.')
  else:
      flash('Artist was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

#----------------------------------------------------------------------------#
# Delete Artists
#----------------------------------------------------------------------------#
@app.route('/artist/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  error = False
  artist_name = ""
  try:
      artist_name = Artist.query.get(artist_id).name
      Artist.query.filter_by(id=artist_id).delete()
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
    flash('An error occurred. Artist ' + artist_name + ' could not be deleted.')
  else:
    flash('Artist ' + artist_name + ' was successfully deleted!')

  return redirect(url_for('index'), code=200)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  upcoming = Show.query.filter(Show.start_time > datetime.now()).all()
  shows = []

  for show in upcoming:
      shows.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch. | OK! I will not! :)
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')

      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()

  if error:
      flash('An error occurred. Show could not be listed.')
  else:
      flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
