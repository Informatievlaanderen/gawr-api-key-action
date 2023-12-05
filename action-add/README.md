# gawr api key action - add

This action generates a new client api key 

## Example
```yaml
name: Add new client apikey
on:
  workflow_dispatch:
    inputs:
      grant-access-road-registry:
        type: boolean
        description: 'Grant road-registry access'
        required: true 
         
      grant-access-sync:
        type: boolean
        description: 'Grant sync access'
        required: true

      client:
        description: 'ClientName'     
        required: true
        
      email:
        description: 'Email'     
        required: true

      plan:
        type: choice
        description: 'Plan'
        options:
        - anon
        - abuse
        - standard
        - unlimited
        default: standard

      apply-env-tst:
        type: boolean
        description: 'Test'
        required: true

      apply-env-stg:
        type: boolean
        description: 'Staging'
        required: true
        
      apply-env-prd:
        type: boolean
        description: 'Production'
        required: true

      apply-env-newprd:
        type: boolean
        description: 'New Production'
        required: true

      access-tickets:
        type: boolean
        description: 'Tickets'
        required: true

jobs:
  gawr:
    runs-on: ubuntu-latest
    steps:
    - name: Add new client apikey
      uses: informatievlaanderen/gawr-api-key-action/action-add@main
      with:
          client:  ${{ github.event.inputs.client }}
          email: ${{ github.event.inputs.email }}
          plan:  ${{ github.event.inputs.plan }}
          
          access-sync:  ${{ github.event.inputs.grant-access-sync }}
          access-road-registry:  ${{ github.event.inputs.grant-access-road-registry }}
          
          env-tst:  ${{ github.event.inputs.apply-env-tst }}
          env-stg:  ${{ github.event.inputs.apply-env-stg }}
          env-prd:  ${{ github.event.inputs.apply-env-prd }}
          env-newprd:  ${{ github.event.inputs.apply-env-newprd }}
          
          aws-tst-access-key-id: ${{ secrets.AWS_TST_ACCESS_KEY_ID }}
          aws-stg-access-key-id: ${{ secrets.AWS_STG_ACCESS_KEY_ID }}
          aws-prd-access-key-id: ${{ secrets.AWS_PRD_ACCESS_KEY_ID }}
          aws-newprd-access-key-id: ${{ secrets.AWS_NEWPRD_ACCESS_KEY_ID }}

          aws-tst-secret-access-key: ${{ secrets.AWS_TST_SECRET_ACCESS_KEY }}
          aws-stg-secret-access-key: ${{ secrets.AWS_STG_SECRET_ACCESS_KEY }}
          aws-prd-secret-access-key: ${{ secrets.AWS_PRD_SECRET_ACCESS_KEY }}
          aws-newprd-secret-access-key: ${{ secrets.AWS_NEWPRD_SECRET_ACCESS_KEY }}
          
          aws-tst-region-name: eu-west-1
          aws-stg-region-name: eu-west-1
          aws-prd-region-name: eu-west-1
          aws-newprd-region-name: eu-west-1

          aws-tst-redis-sync-url: ${{ secrets.AWS_TST_REDIS_SYNC_URL }}
          aws-stg-redis-sync-url: ${{ secrets.AWS_STG_REDIS_SYNC_URL }}
          aws-prd-redis-sync-url: ${{ secrets.AWS_PRD_REDIS_SYNC_URL }}
          aws-newprd-redis-sync-url: ${{ secrets.AWS_NEWPRD_REDIS_SYNC_URL }}
```

### Inputs

|Argument| Description | Default | Required |
|--------|-------------|---------|----------|
| client | The client name | - | Yes |
| email | The client email | - | Yes |
| plan | Plan type `anon`, `abuse`, `standard`, `unlimited` | `anon` | Yes |
| access-sync | Grant sync access (`true` / `false`) | `false` | Yes |
| access-road-registry | Grant road-registry access (`true` / `false`) | `false` | Yes |
| env-tst | Apply in test env. (`true` / `false`) | `false` | Yes |
| env-stg | Apply in staging env. (`true` / `false`) | `false` | Yes |
| env-prd | Apply in production env. (`true` / `false`) | `false` | Yes |
| env-newprd | Apply in new production env. (`true` / `false`) | `false` | Yes |
| aws-tst-access-key-id | AWS access key id test env | - | Yes  |
| aws-stg-access-key-id | AWS access key id staging env | - | Yes  |
| aws-prd-access-key-id | AWS access key id production env | - | Yes  |
| aws-newprd-access-key-id | AWS access key id new production env | - | Yes  |
| aws-tst-secret-access-key | AWS secret access key test env | - | Yes  |
| aws-stg-secret-access-key | AWS secret access key staging env | - | Yes  |
| aws-prd-secret-access-key | AWS secret access key production env | - | Yes  |
| aws-newprd-secret-access-key | AWS secret access key new production env | - | Yes  |
| aws-tst-region-name | AWS region name test env | `eu-west-1` | No |
| aws-stg-region-name | AWS region name staging env | `eu-west-1` | No |
| aws-prd-region-name | AWS region name production env | `eu-west-1` | No |
| aws-newprd-region-name | AWS region name new production env | `eu-west-1` | No |

### Outputs
