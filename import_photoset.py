from app import db, models
import flickr_api


def import_photoset(id):
    # Do some stuff
    account = models.FlickrAccount.query.get(1)
    print account
    #Set the api keys
    flickr_api.set_keys(api_key=account.key, api_secret=str(account.secret))
    auth_handler = flickr_api.auth.AuthHandler(access_token_key=account.oauth_token, access_token_secret=str(account.oauth_secret))

    # Set the authentication handler
    flickr_api.set_auth_handler(auth_handler)
    user = flickr_api.test.login()
    photosets = user.getPhotosets(id=id)
    print photosets
    photoset = [i for i in user.getPhotosets() if i.id == id][0]

    # Create category
    category = models.PhotoCategory()
    category.name = "Trips"
    category.slug = "Vacations and Trips"
    db.session.add(category)

    # Add the photoset to the db
    photoset_db = models.PhotoAlbum(category)
    photoset_db.name = photoset.title
    photoset_db.description = "First visit to San Francisco"
    category.albums.append(photoset_db)
    #db.session.add(photoset_db)


    photos = photoset.getPhotos()
    print photoset
    for photo in photos:
        print photo
        photo_db = models.Photo(photoset_db)
        sizes = photo.getSizes()
        photo_db.thumbnail_path = sizes['Medium 640']['source']
        photo_db.path = sizes['Large 1600']['source']
        print sizes['Medium 640']['source']
        photoset_db.photos.append(photo_db)
        #db.session.add(photo_db)
        #print flickr_api.Photo.getInfo(photo=photo)
        #db.session
    db.session.add(category)
    db.session.commit()

if __name__ == '__main__':
    import_photoset('72157646698322379')
