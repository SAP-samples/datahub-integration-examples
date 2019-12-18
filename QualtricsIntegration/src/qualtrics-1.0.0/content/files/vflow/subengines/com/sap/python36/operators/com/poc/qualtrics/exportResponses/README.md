Export Responses
===

This operator is designed to export responses from a Qualtrics survey in batch mode.
It can export them continously using the `recurrence` configuration parameter. 

Configuration parameters
---

- `API token`: Qualtrics API token, obtained from your Qualtrics account
- `Data Center`: Your Qualtrics account's data center. It's in the format `<datacenter>.qualtrics.com`
- `Survey ID`: The ID of the Qualtrics survey
- `Start Date and Time for initial export`: Defines an initial timestamp from where to start exporting survey responses. If left untouched, first query will return all responses until the moment the operator is run. It works with the `Recurrence` configuration, in the sense that if recurrence is set to a value greater than `0`, it will return only the delta on survey responses.
- `Recurrence`: The frequency you want this operator to extract responses. If left to `0`, the operator will run a single time, otherwise it will run with the specified recurrence.

Output
---

- `responses (string)`: CSV string with responses provided by Qualtrics
- `terminate (string)`: Boolean signal to complete execution of the graph. It will only be used in case `recurrence` is set to `0`.

<br>
<div class="footer">
   &copy; <year> SAP SE or an SAP affiliate company. All rights reserved.
</div>