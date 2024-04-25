from loguru import logger
from datetime import datetime, UTC
import os
import glob
import shutil
import subprocess
import pandas as pd
from app.services.hxmx.dejavu import Dejavu

from app.services.hxmx.picking.utils import (
    recognize_byte_audio_data,
    recognize_audio_data,
    save_pick_results,
    initialize_dejavu,
)
from app.services.hxmx import config
from app.services.hxmx.cleaning.main import clean
from app.services.hxmx.conversion.utils import (
    convert_df_to_wav,
    amplify_package_audio_data,
    amplify_and_segment_sample_data,
    save_audio_to_temp_dir,
    clean_temp_dir,
)


class HxMxPicker:
    def __init__(
        self,
        package_data_dir: str,
        reference_picks_path: str,
        results_dir: str,
        debug: bool = False,
        visualize: bool = False,
        low_memory: bool = False,
    ):
        self.package_data_dir = package_data_dir
        self.reference_picks_path = reference_picks_path
        self.results_dir = results_dir
        self.debug = debug
        self.visualize = visualize
        self.low_memory = low_memory
        self.tops_path = None
        self.picker_args = []

        self._initialize()

    def _initialize(self):

        logger.info("Setting up directories...")
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        results_dir = f"results/results_{timestamp}"
        csv_path = os.path.join(results_dir, "csv")
        self.tops_path = os.path.join(results_dir, "hxmx_tops")

        for pth in [csv_path, self.tops_path]:
            logger.info(pth)
            os.makedirs(pth, exist_ok=True)

        if self.debug:
            logger.info("Debugging is enabled ...")
            debug_dir = os.path.join(results_dir, "debug")
            self.picker_args.extend(["--debug_path", debug_dir])

            debug_paths = [
                os.path.join(debug_dir, "filtered_csv"),
                os.path.join(debug_dir, "audio_data/sample"),
                os.path.join(debug_dir, "audio_data/package"),
                os.path.join(debug_dir, "amplify_package_export/sample"),
                os.path.join(debug_dir, "amplify_package_export/package"),
                os.path.join(debug_dir, "amplify_package_export/convert_df_to_wav"),
            ]
            for pth in debug_paths:
                logger.info(pth)
                os.makedirs(pth, exist_ok=True)

        if self.visualize:
            logger.info("Visualize is enabled ...")
            vis_dir = os.path.join(results_dir, "visualize_data")

            self.picker_args.extend(["--visualize_path", vis_dir])

            vis_paths = [
                os.path.join(vis_dir, "cleanedAudioFiles"),
                os.path.join(vis_dir, "countDfs"),
                os.path.join(vis_dir, "visualResults"),
                os.path.join(vis_dir, "visualResults"),
            ]
            for pth in vis_paths:
                logger.info(pth)
                os.makedirs(pth, exist_ok=True)

        if self.low_memory:
            logger.info("Low Memory is enabled ...")
            self.picker_args.extend(["--low_memory"])

    def run(self):
        csv_files = glob.glob(os.path.join(self.package_data_dir, "*.csv"))

        package_csv_path = os.path.join(self.results_dir, "csv/package_data.csv")
        if len(csv_files) > 0:
            logger.info("Using provided csv file, skiping run_lasToCsv.py")
            input_csv_path = csv_files[0]
            shutil.copy(input_csv_path, package_csv_path)
        else:
            logger.info("Running lasToCsv...")
            run_las_cmd = [
                "python",
                "src/run_lasToCsv.py",
                "--las_path",
                self.package_data_dir,
                "--csv_path",
                package_csv_path,
            ]
            logger.info(run_las_cmd)
            subprocess.call(run_las_cmd)

        logger.info(f"input_csv_path: {package_csv_path}")
        logger.info("Running tops picker...")
        self.hxmx_picker_main()

        if self.visualize:
            vis_cmd = [
                "python",
                "src/run_visualize.py",
                "--package_data",
                os.path.join(
                    self.results_dir, "hxmx_tops/prepocessed_package_data.csv"
                ),
                "--hxmx_picks_path",
                os.path.join(self.results_dir, "hxmx_tops/hxmx_inference_picks.csv"),
                "--reference_picks_path",
                self.reference_picks_path,
                "--save_path",
                os.path.join(self.results_dir, "visualize_data/visualResults"),
                "--count_df_path",
                os.path.join(self.results_dir, "visualize_data/countDfs"),
            ]
            logger.info(vis_cmd)
            subprocess.call(vis_cmd)

    def pick_byte_tops(self, sample_data: list[dict[str, bytes]], djv: Dejavu):
        """_summary_

        Parameters
        ----------
        sample_data : list
            This contains all of the data to be fingerlogger.infoed against.
            It is a list of dicts, the dict has the below format:
            {"formation_name": "byte audio data"}
        djv : dejavu instance
            instance of the dejavu class
        output_csv_path : str
            location to save the results to
        """
        try:
            #################################################
            # DEBUGGING
            # logger.info(f"Sample data: {sample_data}")
            # logger.info(f"Sample data type: {type(sample_data)}")
            # logger.info(f"Sample data length: {len(sample_data)}")
            #################################################
            results_list = []

            # Recognize all the audio data and collect results
            for idx, sample in enumerate(sample_data):
                result = recognize_byte_audio_data(djv, sample)
                if result is not None:
                    results_list.extend(result)
                else:
                    logger.warning(
                        "recognize_byte_audio_data returned None for sample with id: %s",
                        idx,
                    )
            return results_list

        except Exception as e:
            logger.error("Error occurred in pick_byte_tops: %s", e)

    def pick_file_tops(self, path_to_dir: str, djv: Dejavu):
        """This function picks the tops from the audio data.

        Parameters
        ----------
        sample_data : list
            This contains all of the data to be fingerlogger.infoed against.
            It is a list of dicts, the dict has the below format:
            {"formation_name": "byte audio data"}
        djv : dejavu instance
            instance of the dejavu class
        output_csv_path : str
            location to save the results to
        """
        try:
            #################################################
            # DEBUGGING
            # logger.info(f"Sample data: {sample_data}")
            # logger.info(f"Sample data type: {type(sample_data)}")
            # logger.info(f"Sample data length: {len(sample_data)}")
            #################################################
            results_list = []

            # Recognize all the audio data and collect results
            for file_name in os.listdir(path_to_dir):
                results_list.extend(
                    recognize_audio_data(
                        djv=djv, audio_dir=path_to_dir, file_name=file_name
                    )
                )
            logger.info("Recognized all audio data")

            return results_list

        except Exception as e:
            logger.error("Error occurred in pick_file_tops: %s", e)

    def hxmx_picker_main(self):
        """This function is the main function for the hxmx picker.
        Args:
            args (argparser): all the arguments from "run_hxmx_tops_picker.py"
        """

        try:
            package_data_csv: pd.DataFrame = pd.read_csv(self.package_data_dir)
            logger.info(f"Cleaning data from {self.package_data_dir}")
            filtered_api_splits, well_package_and_tops = clean(
                package_data_csv=package_data_csv,
                thresh=config.THRESHOLD,
                sample_tops_file_path=self.reference_picks_path,
                min_depth=config.TRIMMED_LOG_DEPTH,
            )
            logger.info("Data cleaned successfully")

            logger.info("Converting data to WAV format")
            audio_dict = convert_df_to_wav(filtered_api_splits)
            logger.info("Data conversion completed")

            test_data: list[dict[str, bytes]] = [
                {k: audio_dict[k]}
                for k in audio_dict.keys()
                if any(test_id in k for test_id in config.test_data_ids)
            ]
            logger.info(f"TEST DATA LENGTH: {len(test_data)}")

            logger.info("Starting audio segmentation")
            amplified_package_data = amplify_package_audio_data(audio_dict)
            segmented_sample_data = amplify_and_segment_sample_data(
                test_data, well_package_and_tops
            )

            djv: Dejavu = initialize_dejavu()
            logger.info("Initialized Dejavu")

            logger.info("Fingerlogger.infoing the audio data")
            logger.info("Testing data length: ", len(test_data))

            ##########################
            # DEBUG
            # Use the below to save audio files to a temp dir
            ##########################
            if config.debug:
                try:
                    logger.info("Saving audio files to src/data/results/audio_data/")
                    save_audio_to_temp_dir(
                        amplified_package_data,
                        directory=os.path.join(
                            config.debug_path, "audio_data/package/"
                        ),
                    )
                    save_audio_to_temp_dir(
                        segmented_sample_data,
                        directory=os.path.join(config.debug_path, "audio_data/sample/"),
                    )
                except Exception as e:
                    logger.error(
                        f"Error saving audio files to {config.debug_path}: {e}"
                    )
            ##########################
            if self.low_memory:
                try:
                    logger.info("Using tmp dirs for fingerlogger.infoing")
                    package_data_dir = save_audio_to_temp_dir(amplified_package_data)
                    logger.info("saved package data to: ", package_data_dir)
                    sample_data_dir = save_audio_to_temp_dir(segmented_sample_data)
                    logger.info("saved sample data to: ", sample_data_dir)
                    djv.fingerprint_directory(
                        package_data_dir, [".wav", ".mp4", ".mp3"]
                    )
                    logger.info("Picking tops and processing data")
                    picked_tops_list = self.pick_file_tops(sample_data_dir, djv)
                    clean_temp_dir([sample_data_dir, package_data_dir])
                except Exception as e:
                    logger.error(f"Error predicting on audio files: {e}")
                    clean_temp_dir([sample_data_dir, package_data_dir])
                    exit(-1)
            else:
                segmented_sample_arr: list[dict[str, bytes]] = [
                    {k: segmented_sample_data[k]}
                    for k in segmented_sample_data.keys()
                    if any(test_id in k for test_id in config.test_data_ids)
                ]
                logger.info("Using byte data for fingerlogger.infoing")
                djv.fingerlogger.info_byte_data(amplified_package_data)
                logger.info("Picking tops and processing data")
                logger.info("Fingerlogger.infos: ", djv.db.get_num_fingerlogger.infos())
                picked_tops_list = self.pick_byte_tops(segmented_sample_arr, djv)
            logger.info("Picking completed")
            save_pick_results(
                picked_tops_list,
                os.path.join(self.results_dir, "hxmx_inference_picks.csv"),
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            exit(-1)

    def prepare_logs_df(self, well_log_data, filter_depth=6500):
        """
        Desc:
        Filters the well log data by depth and returns a DataFrame with the columns 'WELLAPI', 'DEPT(F)', 'RES(OHMM)', 'GR(GAPI)', and 'BULKDENS(G/C3)'.

        Args:
            well_log_data (df):
                Pandas DataFrame containing the well log data.
            filter_depth (int, optional): filter depth. Defaults to 6500.

        Returns:
            df: filtered pandas dataframe
        """
        # Filter by depth
        return well_log_data[well_log_data["DEPT(F)"] > filter_depth]

    def _read_csv(self, path):
        return pd.read_csv(path)

    def _save_plots(self, figures, save_path, config=None):
        """
        Desc: Saves the provided figures to the specified path.
        Input:
            figures (dict): A dictionary of figure objects to save.
            save_path (str): The base path to save the figures to.
            config (dict): A dictionary of configuration options for the saved figures.
        Output:
            None
        """
        # Ensure the output directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f"Made new directory: {save_path}")

        for fig_data in figures:
            # Ensure the file type is correct
            if str(fig_data["file_id"]).endswith(".html"):
                full_path = os.path.join(save_path, str(fig_data["file_id"]))
            else:
                full_path = os.path.join(save_path, str(fig_data["file_id"]) + ".html")
            fig_data["fig"].write_html(full_path, config=config)
        print(f"Saved: files to {save_path}")

    def visualize_main(self):
        """
        Desc:
            This function is the main function for the visualize module.
            It takes in the arguments from the command line and calls the appropriate functions to visualize the data.
            The main logic is as follows:
                1. Read the data from the files
                2. Create depth subplots
                3. Create count histograms
                4. Create dashboard
                5. Save plots
        """
        cols_to_plot = ["GR(GAPI)_SS", "LOG_RES(OHMM)_SS", "BULKDENS(G/C3)_SS"]

        # Read data
        try:
            logs_df = self._read_csv(self.package_data_dir)
            hxmx_picks_df = self._read_csv(self.results_dir)
            reference_picks_df = self._read_csv(self.reference_picks_path)
        except Exception as e:
            print(f"Error reading files: {e}")
            return

        # Prepare the picks by adding info on it
        hxmx_picks_df["pick_type"] = "hxmx"
        reference_picks_df["pick_type"] = "reference"

        # Printing the head of the dataframes
        print(logs_df.head())
        print(hxmx_picks_df.head())
        print(reference_picks_df.head())

        # Generate depth subplots and histograms
        depth_figures = create_depth_subplots(
            logs_df, reference_picks_df, hxmx_picks_df, cols_to_plot
        )
        self._save_plots(depth_figures, self.save_path)
        if args.count_df_path:
            depth_figures_dict = {fig["file_id"]: fig["fig"] for fig in depth_figures}
            count_histograms_dict = create_count_histograms(args.count_df_path)
            save_plots(count_histograms_dict, args.save_path)
        # histogram_dict = {hist["file_id"].split('_')[0]: hist["fig"] for hist in count_histograms}

        # dashboards = create_wellapi_dashboards(depth_figures_dict, histogram_dict)

        # save_plots(dashboards, args.save_path)
