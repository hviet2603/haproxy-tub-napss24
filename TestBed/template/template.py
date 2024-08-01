from jinja2 import Environment, FileSystemLoader
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--backends', default=8, type=int)
    
    args = parser.parse_args()
    context = {
        'n_backends': args.backends,
        'cache_port_base': 6379,
        'backend_port_base': 3000 
    }

    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)

    targets = ['docker-compose.yaml', 'prometheus.yml', 'haproxy.cfg']
    for target in targets:
        template_file = f"{target}.j2"
        template = env.get_template(template_file)
        output = template.render(context)
        with open(f"./templates/{target}", 'w') as f:
            f.write(output)

if __name__ == "__main__":    
    main()