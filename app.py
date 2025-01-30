from aws_cdk import (
    core as cdk,
    aws_apprunner as apprunner,
    aws_ecr as ecr,
    aws_iam as iam
)

class AppRunnerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an ECR repository
        repository = ecr.Repository(self, "AppRunnerECRRepo",
            repository_name="my-apprunner-repo"
        )

        # Define IAM Role for App Runner
        role = iam.Role(self, "AppRunnerRole",
            assumed_by=iam.ServicePrincipal("build.apprunner.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSAppRunnerServicePolicyForECRAccess")
            ]
        )

        # Deploy App Runner service
        apprunner_service = apprunner.CfnService(
            self, "AppRunnerService",
            service_name="my-app-runner-service",
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn=role.role_arn
                ),
                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier=f"{repository.repository_arn}:latest",
                    image_repository_type="ECR",
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="8080"  # Change this based on your app
                    )
                ),
                auto_deployments_enabled=True
            )
        )

app = cdk.App()
AppRunnerStack(app, "AppRunnerStack")
app.synth()
