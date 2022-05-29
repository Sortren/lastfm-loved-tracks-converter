# Last.fm Loved Tracks To Spotify Playlist
#### Web application that allows the client to get all of the loved tracks from someone's Last.fm profile and make a playlist with it in Spotify

### Technologies used:
<img align = "left" alt = "Python" width = "26px" src = "https://user-images.githubusercontent.com/79079000/118809383-da383580-b8aa-11eb-9b90-b36be1ebd84a.png" />
<img align = "left" alt = "Flask" width = "26px" src = "https://user-images.githubusercontent.com/79079000/130369302-ce7f4c2a-ec15-4f25-a397-371a2c840c50.png" />
<img align = "left" alt = "Typescript" width = "26px" src = "https://user-images.githubusercontent.com/79079000/170893013-76e1adbb-d1c5-4ffa-b279-e8ac10a7dac7.png" />
<img align = "left" alt = "React" width = "26px" src = "https://user-images.githubusercontent.com/79079000/170892959-709ae6de-f916-414c-9873-cd4bca92279a.png" />


<br />

----

### How does it work in general?

1. Client pass the exepcted username from Last.fm service to the form on the frontend. 
2. All of the loved tracks from that user are now fetched by the backend side and displayed for the client
3. Client now clicks that he wants to create a playlist and pass all of the tracks to it, after clicking the button he has to be authorized by the OAuth2.
4. Client gets redirected to the Spotify website to allow access for the app to playlist modifications 
5. After that process, all of the tracks are being sent to the Spotify created playlist.

----
### Configuration
.env file should look like this:
```
API_KEY = api key to the Last.fm service
DEBUG = True/False (if the app are run in the debug mode or not)
SPOTIFY_CLIENT_ID= client id from dev dashboard in spotify
SPOTIFY_CLIENT_SECRET= client secret from dev dashboard in spotify
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/api/v1/spotify-controller/temporary -> link to the page after successful OAuth2 Redirection
```
----
### API Documentation
I have used the Swagger (OpenAPI) from Flask-Restx module, to get auto-generated docs and proper args/req body in endpoints <br />

To display the docs, after running up the server, get to the endpoint:
```
http://127.0.0.1:5000/api/v1/docs
```
You will see smth like this:
![image](https://user-images.githubusercontent.com/79079000/170893502-09a32226-1455-42d9-be3d-dde80d300ffa.png) <br />

You can easily check what is the expected request body or what are the expected arguments of particular endpoint
![image](https://user-images.githubusercontent.com/79079000/170893564-4bbebebb-6239-44b8-ab17-121de5377378.png)

