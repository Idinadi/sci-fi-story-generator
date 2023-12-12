# sci-fi-story-generator
The Science Fiction Story Generator is an innovative application designed to ignite the imagination of sci-fi enthusiasts and writers alike 

## Steps
<ol>
  <li> Download the Science Fiction model from the given google drive link </li>
  https://drive.google.com/drive/folders/1fL5Pp6U5KyHApGde_xsRmZ7WpG2IlhQC?usp=drive_link
  <li> Download the app.py from the given GitHub repository link </li>
  <li> Run the command  in the terminal where you python file and the model is saved: </li>
                    uvicorn app:app --reload
  <li> Got to : </li>
                    http://127.0.0.1:8000/docs
  <li> In the interactive documentation, locate the /stories/ endpoint.    </li>
  <li> You will see a "Try it out" button. Click on it. </li>
  <li> Enter a prompt in the request body. It should be a JSON object with a key named prompt. For example: </li>
              {
                  "prompt": "kid in the backyard saw bunch of heroes"
               }
</ol>

