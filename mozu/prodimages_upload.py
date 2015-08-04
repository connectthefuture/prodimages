
import requests;
import json;
 
auth_url = "https://home.staging.mozu.com/api/platform/applications/authtickets";
tenant_url = "https://t11146.staging-sb.mozu.com/";
headers = {'Content-type': 'application/json', 'Accept-Encoding': 'gzip, deflate'}
 
auth_request = {'applicationId' : 'bluefly.product_images.1.0.0.release', 'sharedSecret' : '53de2fb67cb04a95af323693caa48ddb'};
auth_response = requests.post(auth_url, data=json.dumps(auth_request),  headers=headers, verify=False);
 
print "Auth Response: %s" %auth_response.status_code
auth_response.raise_for_status();
 
auth = auth_response.json();
print "Auth Ticket: %s" %auth["accessToken"];
 
documentApi = tenant_url+"/api/content/documentlists/files@mozu/documents";
documentPayload = {'listFQN' : 'files@mozu', 'documentTypeFQN' : 'image@mozu', 'name' : '{PRODUCT_ID}.JPG', 'extension' : 'jpg'};
 
headers = {'Content-type': 'application/json',  'x-vol-app-claims' : auth["accessToken"], 'x-vol-tenant' : '11146', 'x-vol-master-catalog' : '1'};
 
document_response = requests.post(documentApi, data=json.dumps(documentPayload), headers=headers, verify=False);
document_response.raise_for_status();
 
document = document_response.json();
documentId = document["id"];
 
print "document Id: %s" %documentId;
 
documentUploadApi = tenant_url+"/api/content/documentlists/files@mozu/documents/"+documentId+"/content";
#files = {'media': open("c:\mozu-dc-logo.png", "rb")};
fileData = open('c:\mozu-dc-logo.png', 'rb').read();
headers["Content-type"] = "image/png";
 
content_response = requests.put(documentUploadApi, data=fileData, headers=headers, verify=False);
print "Document content upload Response: %s" %content_response.status_code;
document_response.raise_for_status();
