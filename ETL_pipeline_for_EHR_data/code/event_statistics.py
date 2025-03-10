import time
import pandas as pd
import numpy as np

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    '''
    TODO : This function needs to be completed.
    Read the events.csv and mortality_events.csv files. 
    Variables returned from this function are passed as input to the metric functions.
    '''
    events = pd.read_csv(filepath + 'events.csv')
    mortality = pd.read_csv(filepath + 'mortality_events.csv')

    return events, mortality

def event_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the event count metrics.
    Event count is defined as the number of events recorded for a given patient.
    '''

    dead_df = pd.merge(mortality, events, how='left', on=['patient_id'])
    dead_counts = dead_df.groupby('patient_id').size()
    avg_dead_event_count = dead_counts.mean()
    max_dead_event_count = dead_counts.max()
    min_dead_event_count = dead_counts.min()

    alive_df = events[~events.patient_id.isin(dead_df.patient_id)]
    alive_counts = alive_df.groupby('patient_id').size()
    avg_alive_event_count = alive_counts.mean()
    max_alive_event_count = alive_counts.max()
    min_alive_event_count = alive_counts.min()

    return min_dead_event_count, max_dead_event_count, avg_dead_event_count, min_alive_event_count, max_alive_event_count, avg_alive_event_count

def encounter_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the encounter count metrics.
    Encounter count is defined as the count of unique dates on which a given patient visited the ICU. 
    '''
    dead_df = pd.merge(mortality, events, how='left', on=['patient_id'])
    # print(dead_df.columns)
    dead_dates = dead_df.groupby('patient_id').timestamp_y.nunique()
    avg_dead_encounter_count = dead_dates.mean()
    max_dead_encounter_count = dead_dates.max()
    min_dead_encounter_count = dead_dates.min()

    alive_df = events[~events.patient_id.isin(dead_df.patient_id)]
    alive_dates = alive_df.groupby('patient_id').timestamp.nunique()
    avg_alive_encounter_count = alive_dates.mean()
    max_alive_encounter_count = alive_dates.max()
    min_alive_encounter_count = alive_dates.min()

    return min_dead_encounter_count, max_dead_encounter_count, avg_dead_encounter_count, min_alive_encounter_count, max_alive_encounter_count, avg_alive_encounter_count

def record_length_metrics(events, mortality):
    '''
    TODO: Implement this function to return the record length metrics.
    Record length is the duration between the first event and the last event for a given patient. 
    '''
    dead_df = pd.merge(mortality, events, how='left', on=['patient_id'])
    dead_df['timestamp_y'] = pd.to_datetime(dead_df['timestamp_y'])
    dead_events = dead_df.groupby(['patient_id']).agg(min_date=('timestamp_y', np.min), max_date=('timestamp_y', np.max))
    dead_events['length'] = (dead_events['max_date'] - dead_events['min_date']).dt.days
    avg_dead_rec_len = dead_events['length'].mean()
    max_dead_rec_len = dead_events['length'].max()
    min_dead_rec_len = dead_events['length'].min()

    alive_df = events[~events.patient_id.isin(dead_df.patient_id)]
    alive_df['timestamp'] = pd.to_datetime(alive_df['timestamp'])
    alive_events = alive_df.groupby(['patient_id']).agg(min_date=('timestamp', np.min), max_date=('timestamp', np.max))
    alive_events['length'] = (alive_events['max_date'] - alive_events['min_date']).dt.days
    avg_alive_rec_len = alive_events['length'].mean()
    max_alive_rec_len = alive_events['length'].max()
    min_alive_rec_len = alive_events['length'].min()

    return min_dead_rec_len, max_dead_rec_len, avg_dead_rec_len, min_alive_rec_len, max_alive_rec_len, avg_alive_rec_len

def main():
    '''
    DO NOT MODIFY THIS FUNCTION.
    '''
    # You may change the following path variable in coding but switch it back when submission.
    train_path = '../data/train/'

    # DO NOT CHANGE ANYTHING BELOW THIS ----------------------------
    events, mortality = read_csv(train_path)

    #Compute the event count metrics
    start_time = time.time()
    event_count = event_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute event count metrics: " + str(end_time - start_time) + "s"))
    print(event_count)

    #Compute the encounter count metrics
    start_time = time.time()
    encounter_count = encounter_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute encounter count metrics: " + str(end_time - start_time) + "s"))
    print(encounter_count)

    #Compute record length metrics
    start_time = time.time()
    record_length = record_length_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute record length metrics: " + str(end_time - start_time) + "s"))
    print(record_length)
    
if __name__ == "__main__":
    main()
