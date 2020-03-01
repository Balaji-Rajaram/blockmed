pragma solidity 0.4.25;
pragma experimental ABIEncoderV2;



contract blockmed{
    struct manifucture_data{
        string name;
        string manifucture_address;
        string weight;
        string manifucture_date;
        string expiry_date;
    }
    
    struct distributor_data{
        string name;
        string distributor_address;
        string recived_time;
        string transport_by;
        
    }
    
    mapping(string=>manifucture_data)m_data;
    mapping(string=>distributor_data)d_data;
    
    function manfucture_entry(string med_id,string m_name,string m_address,string weight,string m_date,string e_date)public{
        m_data[med_id].name=m_name;
        m_data[med_id].manifucture_address=m_address;
        m_data[med_id].weight=weight;
        m_data[med_id].manifucture_date=m_date;
        m_data[med_id].expiry_date=e_date;
    }
    
    function distributor_entry(string med_id,string d_name,string d_address,string recived_time,string transport_by)public{
        d_data[med_id].name=d_name;
        d_data[med_id].distributor_address=d_address;
        d_data[med_id].recived_time=recived_time;
        d_data[med_id].transport_by=transport_by;
    }
    function dis_data(string med_id)public view returns(string,string,string,string){
        return(d_data[med_id].name,d_data[med_id].distributor_address,d_data[med_id].recived_time,d_data[med_id].transport_by);
    }
    function manf_data(string med_id)public view returns(string,string,string,string,string){
        return(m_data[med_id].name,m_data[med_id].manifucture_address,m_data[med_id].weight,m_data[med_id].manifucture_date,m_data[med_id].expiry_date);
    }
}