import flickrapi
import webbrowser
from dateutil.parser import parse

api_key = u'9dbfb4b394b8c19fab6075daa12cb45e'
api_secret = u'88e19d1ec44d9c96'
verifier_code = "444-242-724"
my_fliker_user = "196610763@N04"


def start_flickr_session(api_key: str, api_secret: str, verifier_code: str):

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    try:
        flickr.get_access_token(verifier_code)

    except:
        # Only do this if we don't have a valid token already
        if not flickr.token_valid(perms='read'):
            print('Step 1: authenticate')

            # Get a request token
            flickr.get_request_token(oauth_callback='oob')

            # Open a browser at the authentication URL. Do this however
            # you want, as long as the user visits that URL.
            authorize_url = flickr.auth_url(perms='read')
            webbrowser.open_new_tab(authorize_url)

            # Get the verifier code from the user. Do this however you
            # want, as long as the user gives the application the code.
            verifier = str(input('Verifier code: '))

            # Trade the request token for an access token
            flickr.get_access_token(verifier)
        else:
            pass

    return flickr


def get_data(photo_album_name: str, api_key: str, my_fliker_user:str, flickr):

    photo_album_name = photo_album_name

    albums = flickr.photosets.getList(user_id=my_fliker_user)
    photo_album_dict_list = albums["photosets"]["photoset"]

    # get the list of pictures contained in the album
    for photo_album_dict in photo_album_dict_list:
        if photo_album_dict["title"]["_content"] == photo_album_name:
            print("Photo album:", photo_album_name, "found")
            # photo_album_id = photo_album_dict["pk"]
            photo_album_id = photo_album_dict["id"]
            # print(photo_album_dict["title"]["_content"])
            # print(photo_album_dict)
            photos_dict_list = flickr.photosets.getPhotos(api_key=api_key, photoset_id=photo_album_id,
                                                          user_id=my_fliker_user)
            print("containing", len(photos_dict_list), "photos")
        else:
            print(photo_album_name, "does not exist")

    photo_sizes_info_dict = {}
    #     using the list of picture pk get the sizes and the info for each picture
    print("Acquiring info on ", len(photos_dict_list["photoset"]["photo"]), "photos")

    for photos_dict in photos_dict_list['photoset']['photo']:
        # size_info = flickr.photos.getSizes(api_key=api_key, photo_id=photos_dict["pk"]),
        size_info = flickr.photos.getSizes(api_key=api_key, photo_id=photos_dict["id"]),
        info = flickr.photos.getInfo(api_key=api_key, photo_id=photos_dict["id"], secret=photos_dict["secret"])
        photo_sizes_info_dict[photos_dict["id"]] = {"size_info": size_info,
                                                    "info": info
                                                    }

    slide_dict = {}

    print('putting the info on size and url of', len(photo_sizes_info_dict), "photos")
    for photos_id, photo_size_info in photo_sizes_info_dict.items():

        datetime_obj = parse(photo_size_info["info"]['photo']["dates"]["taken"])
        date_time_dict = {'year': datetime_obj.year,
                          'month': datetime_obj.month,
                          'day': datetime_obj.day,
                          'hour': datetime_obj.hour,
                          'minute': datetime_obj.minute,
                          'second': datetime_obj.second
                          }

        photo_date_taken = photo_size_info["info"]["photo"]["dates"]["taken"]
        photo_date_taken_obj = datetime_obj
        photo_date_taken_dict = date_time_dict
        photo_credit = photo_size_info["info"]["photo"]["owner"]["username"]
        photo_title = photo_size_info["info"]["photo"]["title"]["_content"]
        photo_desc = photo_size_info["info"]["photo"]["description"]["_content"]
        photo_original_link = None
        photo_thumbnail_link = None
        # print(photo_size_info["size_info"][0]["sizes"]["size"])
        for size_dict in photo_size_info["size_info"][0]["sizes"]["size"]:
            if size_dict["label"] == 'Original':
                photo_original_link = size_dict['source']
            if size_dict["label"] == 'Thumbnail':
                photo_thumbnail_link = size_dict['source']

        slide_dict[photos_id] = {"photo_date_taken": photo_date_taken,
                                 "photo_date_taken_obj": photo_date_taken_obj,
                                 "photo_date_taken_dict": photo_date_taken_dict,
                                 "photo_credit": photo_credit,
                                 "photo_title": photo_title,
                                 "photo_desc": photo_desc,
                                 "link_to_original_photo": photo_original_link,
                                 "photo_thumbnail_link": photo_thumbnail_link
                                 }

    return slide_dict