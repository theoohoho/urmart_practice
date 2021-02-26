from crontab import CronTab
import os
import sys
import subprocess

root_dir = os.getenv('PYTHONPATH')
if not root_dir:
    raise NameError('PYTOHNPATH is None, please setup PYTHONPATH first, or source setup.py')


def get_file_path() -> (str, str):
    """Get analysis script path and setup log file path
    """
    schedule_worker_path = os.path.join(root_dir, 'schedule_worker')
    execute_script_path = os.path.join(schedule_worker_path, 'analytic.py')
    logfile_path = os.path.join(schedule_worker_path, 'debug.log')
    if not os.path.isfile(execute_script_path):
        raise FileNotFoundError(
            f'Execute script not found: {execute_script_path}')
    return execute_script_path, logfile_path


def get_service_cmd_executable() -> str:
    """Get service command executable path
    """
    try:
        complete_process = subprocess.run('which service', shell=True, check=True, capture_output=True, text=True)
        return complete_process.stdout.strip()
    except subprocess.CalledProcessError as exc:
        print(f'Get service executable encounter error: {exc}')
        raise


def start_cron_service() -> None:
    """Start cron service
    """
    try:
        service_cmd = get_service_cmd_executable()
        subprocess.run(f'{service_cmd} cron start', shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        print(exc.args)
        print(f'Start cron service encounter error: {exc}')
        raise


def setup_cron_job() -> None:
    """Setup crontab settings
    """
    # setup crontab
    my_cron = CronTab(user='root')
    execute_script_path, logfile_path = get_file_path()
    my_cron.env['PYTHONPATH'] = os.getenv('PYTHONPATH')
    python_executable = sys.executable

    # edit crontab
    my_job = my_cron.new(command=f'{python_executable} {execute_script_path} >> {logfile_path} 2>&1')
    my_job.setall('0 0 * * *')
    my_cron.write()


def main() -> None:
    """Main entry point of schedule worker
    """
    start_cron_service()
    setup_cron_job()


if __name__ == "__main__":
    main()
