pragma solidity 0.4.25;



contract blockmed{
    
    struct manifucture_data{
        string name;
        string Type;
        string licence_num;
        string medicin_name;
        string manifucture_address;
        string manifucture_date;
        string expiry_date;
    }
    
    struct distributor_data{
        string name;
        string Type;
        string licence_num;
        string distributor_address;
        string recived_time;
        string transport_by;
        
    }
    
    struct local_distributor_data{
        string name;
        string Type;
        string licence_num;
        string local_distributor_address;
        string recived_time;
        string transport_by;
        
    }
    
    struct vote{
        uint256 like;
        uint256 dislike;
    }
    
    mapping(string=>manifucture_data)m_data;
    mapping(string=>distributor_data)d_data;
    mapping(string=>local_distributor_data)l_data;
    mapping(string=>vote)votes;
    
    function manfucture_entry(string med_id,string medicin_name,string licence_num,string m_name,string m_address,string m_date,string e_date)public{
        m_data[med_id].name=m_name;
        m_data[med_id].licence_num=licence_num;
        m_data[med_id].medicin_name=medicin_name;
        m_data[med_id].manifucture_address=m_address;
        m_data[med_id].manifucture_date=m_date;
        m_data[med_id].expiry_date=e_date;
        m_data[med_id].Type="Manufacturer";
    }
    
    function distributor_entry(string med_id,string licence_num,string d_name,string d_address,string recived_time,string transport_by)public{
        d_data[med_id].name=d_name;
        d_data[med_id].licence_num=licence_num;
        d_data[med_id].distributor_address=d_address;
        d_data[med_id].recived_time=recived_time;
        d_data[med_id].transport_by=transport_by;
        d_data[med_id].Type="Distributor";
    }
    function local_distributor_entry(string med_id,string licence_num,string l_name,string l_address,string recived_time,string transport_by)public{
        l_data[med_id].name=l_name;
        l_data[med_id].licence_num=licence_num;
        l_data[med_id].local_distributor_address=l_address;
        l_data[med_id].recived_time=recived_time;
        l_data[med_id].transport_by=transport_by;
        l_data[med_id].Type="Local Distributor";
    }
    
    function like_med(string med_id)public{
        votes[med_id].like+=1;
    }
    
    function dislike_med(string med_id)public{
        votes[med_id].dislike+=1;
    }
    
    function dis_data(string med_id)public view returns(string,string,string,string,string){
        return(d_data[med_id].name,d_data[med_id].distributor_address,d_data[med_id].recived_time,d_data[med_id].transport_by,d_data[med_id].Type);
    }
    
    function manf_data(string med_id)public view returns(string,string,string,string,string,string){
        return(m_data[med_id].medicin_name,m_data[med_id].name,m_data[med_id].manifucture_address,m_data[med_id].manifucture_date,m_data[med_id].expiry_date,m_data[med_id].Type);
    }
    
    function local_dis_data(string med_id)public view returns(string,string,string,string,string){
        return(l_data[med_id].name,l_data[med_id].local_distributor_address,l_data[med_id].recived_time,l_data[med_id].transport_by,l_data[med_id].Type);
    }
    
    function med_votes(string med_id)public view returns(uint256,uint256){
        return(votes[med_id].like,votes[med_id].dislike);
    }
    
}