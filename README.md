# chart-renderer
A SPA that renders charts for JSON file. The folloing charts are supported:  
- Sankey Chart
- Parallel coordinates Chart
- Simple Line Chart  

Tech stack used:
- Backend: Flask
- Frontend: HTML/CSS, Bootstrap

## Modules required  
* flask  
* pandas  
* plotly  
* kaleido  

To install all these modules run:
``` 
bash modules.sh 
```

## About the JSON file used:  
The JSON file used is present at file/data_4_3.json. From the 4 columns present in the JSON file, I have only used the 1st 2 columns. The data present there are just numbers and all graphs have been made on these 2 columns.

## Steps to run the webapp:  
1. Create a virtual environment in the main directory after cloning the project
```
pipenv shell
```
2. Install the required modules. Run:
``` 
bash modules.sh 
```
3. Run the webapp:
``` 
python main.py
```

## Issues:  
In this application, an issue that arises is that on using multiple queries one after the other, the same image may be displayed over and over as the browser caches the image. For now, perform a hard refresh(ctrl/cmd + shift + R) to get the correct image. Possible solutions inculde:  
* Adding timestamp to image name(found on stackoverflow)  
* Keeping a counter as the image name which increases by 1 after every query  
