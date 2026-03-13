#include <gazebo/common/Plugin.hh>
#include <gazebo/common/Events.hh>
#include <gazebo/physics/physics.hh>
#include <ignition/math/Vector3.hh>
#include <functional>

namespace gazebo
{
class ConveyorPlugin : public WorldPlugin
{
public:
  void Load(physics::WorldPtr world, sdf::ElementPtr sdf) override
  {
    world_ = world;

    min_x_ = sdf->HasElement("min_x") ? sdf->Get<double>("min_x") : -1.0;
    max_x_ = sdf->HasElement("max_x") ? sdf->Get<double>("max_x") : 1.0;
    min_y_ = sdf->HasElement("min_y") ? sdf->Get<double>("min_y") : -0.25;
    max_y_ = sdf->HasElement("max_y") ? sdf->Get<double>("max_y") : 0.25;
    min_z_ = sdf->HasElement("min_z") ? sdf->Get<double>("min_z") : 0.75;
    max_z_ = sdf->HasElement("max_z") ? sdf->Get<double>("max_z") : 1.15;
    velocity_ = sdf->HasElement("velocity") ? sdf->Get<double>("velocity") : 0.30;

    update_connection_ = event::Events::ConnectWorldUpdateBegin(
      std::bind(&ConveyorPlugin::OnUpdate, this));
  }

private:
  void OnUpdate()
  {
    for (const auto & model : world_->Models()) {
      const auto name = model->GetName();
      if (name.find("box_") != 0) {
        continue;
      }

      const auto pose = model->WorldPose();
      const auto pos = pose.Pos();
      const bool in_region =
        pos.X() > min_x_ && pos.X() < max_x_ &&
        pos.Y() > min_y_ && pos.Y() < max_y_ &&
        pos.Z() > min_z_ && pos.Z() < max_z_;

      if (in_region) {
        model->SetLinearVel(ignition::math::Vector3d(velocity_, 0.0, 0.0));
      }
    }
  }

  physics::WorldPtr world_;
  event::ConnectionPtr update_connection_;
  double min_x_{};
  double max_x_{};
  double min_y_{};
  double max_y_{};
  double min_z_{};
  double max_z_{};
  double velocity_{};
};

GZ_REGISTER_WORLD_PLUGIN(ConveyorPlugin)
}  // namespace gazebo
