#!/usr/bin/env python3

# This file will be used to help match song strings. It is a list of lists.
# Each inner list is one song
# The first name in the inner list we will use as the 'real' name.
# Songs must match one of the entries after cleaning, exactly or with a high scoring fuzzy text match

# List is currently very dirty and used to extract rules for cleaning

SONGS = [["A Little Light"],
         ["Ain’t Gonna’ Work On Maggie’s Farm No More", "Maggies Farm"],
         ["Alabama Getaway"],
         ["All Too Much"],
         ["Althea"],
         ["All Along The Watchtower"],
         ["And We Bid You Goodnight"],
         ["Attics Of My Life", "Attics"],
         ["Around & Around", "Around and Around", "A & A", "A&A"],
         ["Baba O'Riley"],
         ["Beat It On Down The Line"],
         ["Believe It Or Not"],
         ["Bertha"],
         ["Beat It On Down The Line", "BIODTL", "B.I.O.D.T.L"],
         ["Big Boss Man"],
         ["Built To Last"],
         ["Big River"],
         ["Big Boy Pete"],
         ["Bird Song", "Bird Song/Set Break With Carlos Santana", "Birdsong"],
         ["Black Muddy River"],
         ["Black Peter"],
         ["Black Throated Wind", "BT Wind"],
         ["Blow Away", "drops or cuts in Blow Away @4:27", "Blow Away -> wait-a-minute rap -> Blow Away"],
         ["Blues For Allah"],
         ["Box Of Rain"],
         ["Brokedown Palace", "Brokedown..Palace ( End Missing, Patched ** )"],
         ["Broken Arrow"],
         ["Brown Eyed Women"],
         ["Casey Jones", "KC Jones"],
         ["Cassidy"],
         ["Candyman"],
         ["CC Rider", "C.C. Rider", "C. C. Rider"],
         ["Chanting by Guyto Monks", "Guyto Monks"],
         ["China Cat Sunflower"],
         ["Childhood's End"],
         ["China Doll"],
         ["Cold Rain & Snow", "Cold Rain And Snow"],
         ["Comes A Time"],
         ["Corrina"],
         ["Crazy Fingers"],
         ["Cumberland Blues"],
         ["Dark Star"],
         ["Dark Hollow"],
         ["Days Between", "The Days Between"],
         ["Day Job", "Keep Your Day Job"],
         ["Deal"],
         ["Death Don't Have No Mercy"],
         ["Desolation Row"],
         ["Dear Mr. Fantasy", "Dear Mister Fantasy"],
         ["Dire Wolf", "Dire Wolf.. (Ending Notes Cut)"],
         ["Don't Ease", "Don't Ease Me In"],
         ["Drums", "Drums & Mardi Gras Parade*", "Drums continued", "Drums//", "Drumz", "drums", "drums > (tape flip near end)", "Drums.. > ( First Minute Only, Rest MIA on Tape )", "Electronic Percussion", "drums (with Billy Cobham)"],
         ["Drums>Space", "Drums > Space", "D>S", "Drums>Space...(some of space missing)"],
         ["Dupree's Diamond Blues"],
         ["Easy Answers"],
         ["Easy To Love You"],
         ["El Paso"],
         ["Encore Break", "Encore", "Encore Break (Added From Set 1 Tape)", "Encore..Break (Tape Pause Between)"],
         ["Estimated Prophet"],
         ["Eternity"],
         ["Eyes Of The World", "Eyes-> Jam->"],
         ["Far From Me"],
         ["Foolish Heart"],
         ["Friend Of The Devil", "FOTD"],
         ["Feel Like A Stranger", "Stranger"],
         ["Fire On The Mountain", "Fire"],
         ["Franklins Tower"],
         ["Going Down The Road Feeling Bad", "GDTRFB", "G.D.T.R.F.B.", "g.d.t.r.f.b"],
         ["Gimme Some Lovin'"],
         ["Good Time Blues"],
         ["Gloria"],
         ["Good Lovin'", "Good Loving"],
         ["Good Morning Little Schoolgirl"],
         ["Greatest Story", "Greatest Story Ever Told"],
         ["Handsome Cabin Boy"],
         ["Happy Birthday"],
         ["Heaven Help The Fool"],
         ["He's Gone"],
         ["Hell In A Bucket", "Bucket"],
         ["Help On The Way"],
         ["Here Comes Sunshine"],
         ["Hey Jude", "Hey Jude Finale"],
         ["Hey Pocky Way"],
         ["Hi-Heeled Sneakers"],
         ["High Time", "High Time (Tape Flip Directly After, Very End Cut)"],
         ["Hoochie Coochie Man"],
         ["Hully Gully"],
         ["(I Can't Get No) Satisfaction", "(Encore) Satisfaction", "Satisfaction"],
         ["If The Shoe Fits", "Show Fits"],
         ["I Just Want To Make Love To You"],
         ["It's All Over Now", "Used To Love Her"],
         ["It's All Over Now, Baby Blue"],
         ["It Takes A Lot To Laugh, It Takes A Train To cry", "Train To Cry"],
         ["It Must Have Been The Roses"],
         ["I Fought The Law"],
         ["I Know You Rider"],
         ["I Need A Miracle"],
         ["I Want To Tell You"],
         ["I Will Take You Home"],
         ["Iko Iko", "Aiko Aiko", "Aiko-Aiko", "Iko-Iko"],
         ["Intro"],
         ["It's All Over Now, Baby Blue"],
         ["I'm A King Bee"],
         ["I've Been All Around this World"],
         ["Jam", "JAM!", "Jam (2)", "JAM (Bob, Bruce, Jerry)", "two soldiers jam", "bruce and drummers jam", "piano jam"],
         ["Jack A Roe"],
         ["Jack Straw", "jack straw (if you listen, you can hear brett laugh)", "Jack Straw * ( Cuts In, Start Patched ** )"],
         ["Jack-A-Roe"],
         ["Jam", "Mock Turtle Jam"],
         ["Johnny B. Goode", "J.B. Goode", "JB Goode"],
         ["Just A Little Light"],
         ["Just Like Tom Thumb's Blues"],
         ["Knockin' On Heaven's Door"],
         ["Lazy River Road"],
         ["Let It Grow"],
         ["Let The Good Times Roll", "LTGTR"],
         ["Let it Grow"],
         ["Liberty"],
         ["Little Red Rooster"],
         ["Looks Like Rain", "LL Rain", "L.L. Rain"],
         ["Loose Lucy"],
         ["Lost Sailor"],
         ["Lucy In The Sky With Diamonds", "LSD", "L.S.D."],
         ["Loser"],
         ["Maggie's Farm"],
         ["Mama Tried"],
         ["Man Smart (Woman Smarter)", "Man Smart (Women Smarter)", "Man Smart (Women are Smarter)", "Man Smart, Woman Smarter", "Women Are Smarter"],
         ["Mathilda", "Matilda Matilda", "Matilda"],
         ["Me & My Uncle", "Me And My Uncle"],
         ["Memphis Blues Again", "Memphis Blues (First Few Notes Missing)"],
         ["Midnight Hour"],
         ["Might As Well"],
         ["Mind Left Body Jam", "Mind Left Body"],
         ["Minglewood Blues", "All New Minglewood Blues"],
         ["Mississippi Half Step", "Mississippi Half Step Uptown Toodeloo", "Mississippi Half-Step", "Mississippi Half-Step Uptown Toodleloo", "Half-Step", "Half Step"],
         ["Mona"],
         ["Monkey and the Engineer"],
         ["The Mighty Quinn", "Mighty Quinn", "Quinn The Eskimo", "The Mighty Quinn (Quinn The Eskimo)"],
         ["Morning Dew"],
         ["Never Trust A Woman"],
         ["New Minglewood Blues"],
         ["New Speedway Boogie"],
         ["Nobody's Fault Jam", "Nobody's Fault But Mine Jam"],
         ["Not Fade Away", "NFA", "Not Fade..Away> (Tape Flip During,Remaining Added To First Tape)"],
         ["Not Fade Away Chant", "NFS Chant"],
         ["One More Saturday Night", "Saturday Night"],
         ["Peggy-O", "Peggy O", "Fennario"],
         ["Picasso Moon"],
         ["Phil's Earthquake Space"],
         ["Playin' In The Band", "Playin' in the Band", "Playing In The Band", "Playing In the Band", "Playing in the Band", "Playin In The Band", "PITB", "Playin'"],
         ["Playin' Jam", "Playing Jam", "Jam out of Playin"],
         ["Playin' Reprise"],
         ["Promised Land", "Promised..Land, set Break ( Power Loss Inside, Music Starts Back Up )"],
         ["Queen Jane Approximately", "Queen Jane"],
         ["Ramble On Rose", "ROR"],
         ["Rain"],
         ["Rainy Day Women #12 and 35"],
         ["Reuben & Cherise"],
         ["Revolution"],
         ["Ripple"],
         ["Rollin' and Tumblin'"],
         ["Rosalie McFall"],
         ["Row Jimmy", "Row Jimmy (End Missing From Source Tapes *)"],
         ["Saint Of Circumstance"],
         ["Samba In The Rain"],
         ["Set Break", "Set Break, Mickey Hart/Radio"],
         ["Salt Lake City"],
         ["Sampson & Delilah", "Samson"],
         ["Scarlet Begonias"],
         ["Shakedown Street"],
         ["Ship Of Fools"],
         ["Slipknot", "Slipknot!"],
         ["Space", "Spa//ce", "S..pace (Tape Flip At Start)", "Spac..e > (Tape Flip)", "Space > (2)", "space", "Space.. (tape flip after space,some of space missing)", "Space (with locotomotive airhorn) >", "silent way jam > space", "spa/ce"],
         ["Spoonful"],
         ["Smokestack Lightning"],
         ["So Many Roads"],
         ["Stagger Lee"],
         ["St. Stephen"],
         ["Standing On The Moon", "Standing on the Moon", "sotm", "SOTM"],
         ["Stella Blue"],
         ["Stir It Up"],
         ["Stir It Up Jam"],
         ["Stronger Than Dirt"],
         ["Stuck Inside Of Mobile With The Memphis Blues Again", "Stuck Inside Of Mobile"],
         ["Supplication"],
         ["Sugar Magnolia"],
         ["Sunshine Daydream", "SSDD"],
         ["Sugaree"],
         ["Take You Home"],
         ["Take Me To The River"],
         ["That Would be Something"],
         ["Tennessee Jed"],
         ["Terrapin", "Terrapin Station", "Terrapin Station > Jam"],
         ["The Last Time", "This Could Be The Last Time"],
         ["The Music Never Stopped"],
         ["The Race Is On"],
         ["The Other One", "Other One", "TOO"],
         ["The Same Thing"],
         ["The Wheel", "Wheel"],
         ["The Weight", "Crowd - The Weight - Crowd outro"],
         ["They Love Each Other", "TLEO"],
         ["Throwing Stones", "Throwing Stones > {flip} {right channel problems} patched with gastwirt"],
         ["To Lay Me Down"],
         ["Tomorrow Never Knows"],
         ["Tom Thumb Blues", "Tom Thumb's Blues", "Tom Thumbs Blues"],
         ["Touch Of Gray", "Touch Of Grey"],
         ["Truckin'", "Truckin"],
         ["Turn On Your Love Light", "Turn On Your Lovelight", "Lovelight"],
         ["Uncle John's Band"],
         ["U.S. Blues", "US Blues", "US Blues (partial AUD patch)"],
         ["Unbroken Chain"],
         ["Valley Road"],
         ["Victim Or The Crime", "Victim"],
         ["Visions Of Johanna"],
         ["Wave to the Wind"],
         ["Walkin' Blues", "Walking Blues"],
         ["Wang Dang Doodle"],
         ["Way To Go Home"],
         ["We Bid You Good Night"],
         ["We Can Run But We Can't Hide", "We Can Run"],
         ["Werewolves Of London"],
         ["West L.A. Fadeaway", "West LA Fadeaway", "West LA Fadeawy"],
         ["Wharf Rat"],
         ["When I Paint My Masterpiece", "Masterpiece"],

         # obvious guest songs
         ["Do Right Woman, Do Right Man", "Do Right Woman"],
         ["Lady Di"],
         ["Lucifer's Eyes"],
         ["I’ve Got a Mind to Give Up Living", "A Mind to Give Up Livin'"],
         ["Proud Mary"],
         ["Forever Young"],
         ["Greensleeves"],
         ["Bad Moon Rising"],
         ["Flibberty Jib", "Flibberty Jib On The Bippity Bop"],
         ["The Island"],

         # sometime combos come up. Place here and fix later,
         ["MS 1/2 Step>The Weight"],
         ["Crazy Fingers > Playing Jam > Drums > Space >"],
         ["Help On The Way -> Slipknot! -> Franklin's Tower"],
         ["Dark Star jam > Bob/Phil/Bruce jam >"],
         ["Jam* -> Drums ->"],
         ["Jam > Bruce instrumental >"],
         ["Space / Spanish Jam >"],
         ["Space > Flibberty Jib > The Island"],
         ["mama tried-> mexicali blues"],
         ["far from me ; candyman"],

         # weird named jams
         ["Dear Prudence Jam"],

         # oh dear
         ["Cosmic Charlie Tease"],

         # is this a track?
         ["Phil & Keyboards Jam"],
         ["Take A Step Back", "Step Back", "crowd/tuning > take a step back"],
         ["Adams Family"],
         ["Hamza El-Din"],
         ["Ken Nordine's Flibberdy Jib"],
         ["Countdown to Midnight", "Countdown"],
         ["Ken Kesey Rap"],
         ["A Day At The Dentist"],

         # stuff to ignore
         ["encore break"],
         ["Filler", "Filler - Me and Bobby McGee"],
         ["Crowd/Tuning", "Tuning", "We Want Phil'", "Crowd", "./-", "Bill Graham Speech", "its a bullshit lie", "Tuning (taper narrative)", "we want phil - 'there's this rumor goin' round...'"],
        ]
