import subprocess
import logging

from chanjo.log import get_log_stream


def run_sambamba(bam_file, region_file, outfile=None, cov_treshold=()):
    """
    Run sambamba from chanjo.
    
    """
    logger = logging.getLogger(__name__)
    logger = logging.getLogger("chanjo.sambamba")
    log_stream = get_log_stream(logger)
    sambamba_call = [
        "sambamba",
        "depth",
        "region",
        "--regions",
        region_file,
        bam_file
    ]
    
    if outfile:
        sambamba_call += ["-o", outfile]
    
    for coverage_treshold in cov_treshold:
        sambamba_call += ['-T', str(coverage_treshold)]
    
    logger.info("Running sambamba with call:\n{0}".format(' '.join(sambamba_call)))
    
    try:
        subprocess.check_call(
            sambamba_call,
            stderr=log_stream,
        )
    except OSError as e:
        logger.critical("sambamba seems to not exist on your system.")
        sys.exit()
    
    logger.debug("sambamba run successfull")
    
    return