## build-env
This is a docker image for ci building

It is based on a python3 image and the following programs

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
usage: webservice-validation [-h] endpoint validation-spec

positional arguments:
  endpoint
  validation-spec

optional arguments:
  -h, --help       show this help message and exit
```
