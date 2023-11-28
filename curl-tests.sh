curl -X 'GET' \
  'http://127.0.0.1:8000/post/aut_appstatus/' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://127.0.0.1:8000/post/schedule' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://127.0.0.1:8000/post/network/1/content/Testing%20IslabTweet%20%40islabunimi' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "path": "/home/mapto/Dropbox/unimi/tweetpy/islab.jpg"
  }
]'

curl -X 'POST' \
  'http://127.0.0.1:8000/post/network/1/content/Hello%20%40islabunimi%2C%20greetings%20from%20IslabTweet/due/2023-05-09' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "path": "/home/mapto/Dropbox/unimi/tweetpy/islab.jpg"
  }
]'


# failing
curl -X 'GET' \
  'http://127.0.0.1:8000/identity/mapto' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://172.20.27.81:8090/post/content/Hello%20world%21%20This%20is%20my%20first%20tweet?date_sched=2023-06-07&social_network_id=1' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic d2l0dGVydGVzdDU1NTU1OmE=' \
  -H 'Content-Type: application/json' \
  -d '[
  {
  }
]'

curl -X 'POST' \
  'http://wittertest55555@172.20.27.81:8090/post/content/Hello%20world%21%20This%20is%20my%20first%20tweet?date_sched=2023-06-07&social_network_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[{}]'


# This one is too long to flush
curl -X 'POST' \
  'http://mapto@localhost:8090/post/poll/content/%22I%20have%20always%20followed%20the%20practice%20of%20praising%20what%20I%20deemed%20well%20said%20by%20others%2C%20and%20of%20refuting%20what%20was%20badly%20said.%20I%20have%20never%20belittled%20or%20laid%20false%20claim%20to%20the%20ideas%20of%20others%2C%20when%20I%20had%20none%20of%20my%20own.%20I%20have%20never%20fawned%20on%20others%2C%20nor%20have%20I%20been%20self-effacing%20if%20I%20made%20some%20better%20or%20prior%20discovery%20by%20my%20own%20exertions.%22%20-%20Dissertatio%2C%20J.%20Kepler.%20Which%20values%20do%20you%20identify%20in%20the%20text%3F%20%23ScientificRevolution%20%40vastproject%20%40IslabUnimi?opt1=Human%20Dignity&opt2=Integrity&opt3=Evidence&opt4=Experimentation' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://localhost:8090/post/poll/content/%22Free%20in%20mind%20must%20be%20he%20who%20desires%20to%20have%20understanding%22%20-%20Dissertatio%2C%20J.%20Kepler%20%40vastproject%20%40IslabUnimi?opt1=Freedom&opt2=Progress&opt3=Freedom%20vs%20Slavery&opt4=Evidence%20vs%20Authority' \
  -H 'accept: application/json'

%0a

Which values do you identify in this text? "Free in mind must be he who desires to have understanding" - Dissertatio, J. Kepler #ScientificRevolution @vastproject @IslabUnimi

curl -X 'POST' \
  'http://mapto@localhost:8090/post/poll/content/Which%20values%20do%20you%20identify%20in%20this%20text%3F%0a%22Free%20in%20mind%20must%20be%20he%20who%20desires%20to%20have%20understanding%22%20-%20Dissertatio%2C%20J.%20Kepler%0a%23ScientificRevolution%20%40vastproject%20%40IslabUnimi?opt1=Freedom&opt2=Progress&opt3=Freedom%20vs%20Slavery&opt4=Evidence%20vs%20Authority' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://mapto@localhost:8090/post/content/Which%20values%20do%20you%20identify%20in%20this%20text%3F%250a%22Free%20in%20mind%20must%20be%20he%20who%20desires%20to%20have%20understanding%22%250a-%20Dissertatio%2C%20J.%20Kepler%250a%23ScientificRevolution%20%40vastproject%20%40IslabUnimi' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "path": ""
  }
]'

curl -X 'POST' \
  'http://mapto@localhost:8090/post/poll/content/Which%20values%20do%20you%20identify%20in%20this%20text%3F%250a%22Yet%20I%20hold%20that%20completely%20erroneous%20views%20should%20be%20shunned%22%250a-%20De%20revolutionibus%20orbium%20coelestium%2C%20N.%20Copernicus%250a%23ScientificRevolution%20%40vastproject%20%40IslabUnimi?opt1=Freedom&opt2=Demonstrable%20Truth&opt3=Tolerance&opt4=Kindness&duration_minute=10080&social_network_id=1' \
  -H 'accept: application/json'