from spaghetti.filtering.interface import ProjectDependenciesFilter
from spaghetti.models.project_dependencies import ProjectDependencies


class HideModulesWithoutLinksFilter(ProjectDependenciesFilter):
    def apply_filter(self, dependencies: ProjectDependencies) -> ProjectDependencies:
        return ProjectDependencies(
            module_imports={
                module: links
                for module, links in dependencies.module_imports.items()
                if len(links) > 0
            }
        )
