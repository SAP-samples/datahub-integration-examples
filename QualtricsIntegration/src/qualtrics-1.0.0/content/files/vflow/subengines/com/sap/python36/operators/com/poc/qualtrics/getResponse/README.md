Get Response
===

Operator designed to extract a full response from a Qualtrics survey, provided its ID. Ideally used with with an API receiving response IDs from Qualtrics.

Configuration parameters
---

- `API token`: Qualtrics API token, obtained from your Qualtrics account
- `Data Center`: Your Qualtrics account's data center. It's in the format `<datacenter>.qualtrics.com`
- `Survey ID`: The ID of the Qualtrics survey

Input
---

- `responseID (string)`: a json string with the response ID in format `{'responseID': response-id}`.

Output
---

- `response (string)`: CSV string of the full response, provided by Qualtrics

<br>
<div class="footer">
   &copy; <year> SAP SE or an SAP affiliate company. All rights reserved.
</div>