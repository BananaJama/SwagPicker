using namespace System.Net

# Input bindings are passed in via param block.
param($Request, $TriggerMetadata)

# Write to the Azure Functions log stream.
Write-Host "PowerShell HTTP trigger function processed a request."

# Interact with query parameters or the body of the request.
<#
$name = $Request.Query.Name
if (-not $name) {
    $name = $Request.Body.Name
}
#>
$Params = $Request.body | ConvertFrom-Json
$FirstName = $Params.fname
$LastName = $Params.lname

$body = "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."


if ($FirstName -and $LastName) {
    $body = "Hello $LastName, $FirstName. This HTTP triggered function executed successfully."
}

# Associate values to output bindings by calling 'Push-OutputBinding'.
Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = $body
})

Push-OutputBinding -Name FullName -Value "$LastName,$FirstName"