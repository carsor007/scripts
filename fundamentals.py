from micropyramid.process import wakeup_and_get_design, prepare_recipe,report_to,report_and_freak
from client import project

def deliver_awesome(pyramid):
    prepare_recipe(pyramid.ingredients)
    if not design_ready:
        wakeup_and_get_design(pyramid.designer, bootstrap, html5, CSS3)
    else:
        try:
            push_to_live if pyramid_pass_on_stage else report_to(pyramid.dev)
            check_load_balancer(pyramid, get_aws(pyramid.ingredients))
            return "Awesome!"
        except any_thing:
            report_and_freak(pyramid.all)
            return "Repeat till awesome"

if __name__== "__main__":
        project.ingredients = ['django', 'elasticsearch', 'less',
                               'bootstrap', 'angular', 'postgress', 'aws']
        deliver_awesome(project)
