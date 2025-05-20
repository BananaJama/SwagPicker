from flask import Flask, render_template, request
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
from dotenv import load_dotenv
load_dotenv()
import os
import random


app = Flask(__name__)

TABLE_NAME = "swagIdentities"
STORAGE_ACCOUNT_CREDENTIAL = AzureNamedKeyCredential(os.getenv("STORAGE_ACCOUNT_NAME"),os.getenv("STORAGE_ACCOUNT_KEY"))
# Initialize the TableServiceClient
#credential = DefaultAzureCredential()
table_client = TableServiceClient(
    endpoint=os.getenv("STORAGE_ACCOUNT_ENDPOINT"),
    credential=STORAGE_ACCOUNT_CREDENTIAL
)
swagIdentitiesTable = table_client.get_table_client(TABLE_NAME)

@app.route('/')
def home():
   return render_template('index.html')

@app.post('/processIdentity')
def processIdentity():
   name = request.form['name']
   email = request.form['email']
   print(f"Received value: {name}, {email}")
   
   entity = {
       'PartitionKey': 'SwagId',
       'RowKey': email,
       'Name': name,
       'Email': email
   }
   swagIdentitiesTable.create_entity(entity=entity)
   return render_template('processIdentity.html', name=name, email=email)


@app.get('/getSwagIdentities')
def getSwagIdentities():
   swagIdentities = []
   for i in swagIdentitiesTable.list_entities():
      swagIdentity = {
         'Name': i['Name'],
         'Email': i['Email']
      }
      swagIdentities.append(swagIdentity)
   return render_template('listIdentities.html', swagIdentities=swagIdentities)

@app.get('/getSwagger')
def getSwagger():
   swagIdentities = []
   for i in swagIdentitiesTable.list_entities():
      swagIdentity = {
         'Name': i['Name'],
         'Email': i['Email']
      }
      swagIdentities.append(swagIdentity)
   winner = random.choice(swagIdentities)
   return render_template('winner.html', winner=winner) 

if __name__ == '__main__':
   app.run(debug=True)