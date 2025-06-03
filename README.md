## build-env
This is a docker image for ci building.

The image is based on the python3 base image and contains a sonar-scanner binary and the following executables:

### deploy-versioner
A program for automatic setting new versions in kubernetes deployment
configurations, meant for a gitops workflow.

https://github.com/DBCDK/kube-deployment-auto-committer

#### Help
```
$ set-new-version -h
usage: set-new-version [-h] [-b BRANCH] [--gitlab-url GITLAB_URL] [-n]
                       deployment-configuration gitlab-api-token project-name
                       image-tag

positional arguments:
  deployment-configuration
                        filename or dir of deployment configuration to change.
                        If a dir is specified, all .yaml and .yml files in
                        that dir recursively will be included.
  gitlab-api-token      private token for accessing the gitlab api
  project-name          Name of project (including group hierarchy), e.g.,
                        metascrum/rrflow-deploy
  image-tag             new tag to commit into the deployment configuration

optional arguments:
  -h, --help            show this help message and exit
  -b BRANCH, --branch BRANCH
  --gitlab-url GITLAB_URL
  -n, --dry-run         don't commit changes, print them to stdout

```

### webservice-validation
A program for validating responses from a webservice.

The validation spec must be yaml and consist of a list of validation objects.
The format will likely change slightly as we begin to use it and
discover shortcomings.

The specific part of the response to be validated (at the moment
validation means checking if the object has a length equal to or greater
than the value specified by `response.len` in the validation spec with a
default of 1) can be extracted with jsonpath using
`response.jsonpath`. All of the jsonpath specification is supported, but
only the most simple use-cases are tested as of the initial commit.
- <https://goessner.net/articles/JsonPath/>
- <https://pypi.org/project/jsonpath-ng/>

To test against multiple endpoints you can supply a json file with a
list of endpoints to test. The format must be a list of objects
containing an `ip` key with the endpoint. This output can be fetched
from the `kube-tools ip-addresses` command (<https://gitlab.dbc.dk/ai/kube-tools-rs>).
It looks like this
```
[
    {
        "ip": "10.233.22.82",
        "name": "subject-suggester-1-0-7c785b866c-gp5dz"
    },
    {
        "ip": "10.233.33.145",
        "name": "subject-suggester-1-0-7c785b866c-ltxc7"
    },
    {
        "ip": "10.233.2.143",
        "name": "subject-suggester-1-0-7c785b866c-ss82s"
    }
]
```
When testing with output from the `kube-tools` command be aware if you
need to also specify the port to use on the endpoint. You can do that
with `-p` or `--port`.

Ex:
```yaml
- validation:
  path: /api/subjects/related/emne?record_id=validation-test
  method: post
  data: '["666*fhistorie", "666*fpolitik"]'
  response:
    jsonpath: "response"
    status_code: 200
  headers: {"content-type": "application/json"}
```

#### Help
```
$ webservice-validation -h
usage: webservice-validation [-h] [--from-endpoints-json-file FROM_ENDPOINTS_JSON_FILE] [-p PORT] endpoint validation-spec

positional arguments:
  endpoint
  validation-spec

optional arguments:
  -h, --help            show this help message and exit
  --from-endpoints-json-file FROM_ENDPOINTS_JSON_FILE
                        Validate from a list of endpoints instead of the single positional argument endpoint. The format should be a list of object containing an `ip`
                        key with the endpoint. This output can be fetched with the `kube-tools ip-addresses` command.
  -p PORT, --port PORT  Port to query on the service which is to be validated.
```

#### Examples
```
kube-tools ip-addresses mi-staging app=simple-search-1-0 | webservice-validation from-endpoints-json-file deploy/validation.yml --from-endpoints-json-file - -p 5000
```
